SHELL := /bin/bash

ANSIBLE_DIR := ansible
ANSIBLE_INVENTORY := $(ANSIBLE_DIR)/inventories/env_inventory.py
ANSIBLE_DEPLOY_PLAYBOOK := $(ANSIBLE_DIR)/playbooks/deploy-app.yml
ANSIBLE_LOCAL_TEMP ?= /tmp/ansible-local-tmp
ANSIBLE_ENV := ANSIBLE_LOCAL_TEMP=$(ANSIBLE_LOCAL_TEMP) ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=$(ANSIBLE_DIR)/ansible.cfg

ZONE ?= all
TAG ?= latest
DEPLOY_EXTRA_VARS = deploy_zone=$(ZONE) deploy_image_tag=$(TAG)

.PHONY: help deploy deploy-zone deploy-edu deploy-ebook deploy-ping deploy-syntax-check docker-prune-vps generate-pdfs seed-edu seed-ebook seed

help:
	@printf "Galura SLiMS Ansible Deployment Commands (Local Build -> Direct Push -> Auto Prune)\n\n"
	@printf "  make deploy-ping                    Test koneksi SSH VPS dari .env\n"
	@printf "  make deploy-syntax-check            Validasi syntax Ansible Playbook\n"
	@printf "  make deploy                         Build lokal, transfer ke VPS, run & prune image (semua zone)\n"
	@printf "  make deploy-zone ZONE=edu           Deploy zone edu (slims-edu.galura.id)\n"
	@printf "  make deploy-zone ZONE=ebook         Deploy zone ebook (slims-ebook.galura.id)\n"
	@printf "  make deploy-edu                     Shortcut deploy zone edu\n"
	@printf "  make deploy-ebook                   Shortcut deploy zone ebook\n"
	@printf "  make docker-prune-vps               Hapus image docker gantung / tidak dipakai di VPS\n"
	@printf "  make generate-pdfs                  Generate sampel PDF 3-halaman realistis lokal\n"
	@printf "  make seed-edu                       Import dummy seed koleksi buku fisik ke SLiMS Edu\n"
	@printf "  make seed-ebook                     Generate PDF, upload ke VPS, dan import seed SLiMS Ebook\n"
	@printf "  make seed                           Jalankan seed data lengkap untuk SLiMS Edu dan Ebook\n"

$(ANSIBLE_LOCAL_TEMP):
	mkdir -p $(ANSIBLE_LOCAL_TEMP)

deploy-ping: $(ANSIBLE_LOCAL_TEMP)
	$(ANSIBLE_ENV) ansible -i $(ANSIBLE_INVENTORY) webservers -m ping

deploy-syntax-check: $(ANSIBLE_LOCAL_TEMP)
	$(ANSIBLE_ENV) ansible-playbook -i $(ANSIBLE_INVENTORY) $(ANSIBLE_DEPLOY_PLAYBOOK) --syntax-check
	$(ANSIBLE_ENV) ansible-playbook -i $(ANSIBLE_INVENTORY) $(ANSIBLE_DIR)/playbooks/site.yml --syntax-check

deploy: $(ANSIBLE_LOCAL_TEMP)
	$(ANSIBLE_ENV) ansible-playbook -i $(ANSIBLE_INVENTORY) $(ANSIBLE_DEPLOY_PLAYBOOK) --extra-vars "deploy_zone=all deploy_image_tag=$(TAG)"

deploy-zone: $(ANSIBLE_LOCAL_TEMP)
	$(ANSIBLE_ENV) ansible-playbook -i $(ANSIBLE_INVENTORY) $(ANSIBLE_DEPLOY_PLAYBOOK) --extra-vars "$(DEPLOY_EXTRA_VARS)"

deploy-edu:
	$(MAKE) deploy-zone ZONE=edu TAG="$(TAG)"

deploy-ebook:
	$(MAKE) deploy-zone ZONE=ebook TAG="$(TAG)"

docker-prune-vps: $(ANSIBLE_LOCAL_TEMP)
	$(ANSIBLE_ENV) ansible -i $(ANSIBLE_INVENTORY) webservers -m command -a "docker image prune -f"

generate-pdfs:
	python3 database/seeds/generate_pdfs.py

seed-edu:
	@echo "==> Mengimport seed data buku fisik ke senayan_edu..."
	ssh -i $(shell grep DEPLOY_SSH_KEY .env | cut -d= -f2) $(shell grep DEPLOY_SSH_USER .env | cut -d= -f2)@$(shell grep DEPLOY_SSH_IP .env | cut -d= -f2) \
		"sudo docker exec -i galura-slims-edu-db mariadb -u root -p'$(shell grep DB_PASS_EDU .env | cut -d= -f2)' senayan_edu" < database/seeds/seed_edu.sql
	@echo "==> [SUKSES] Seed data SLiMS EDU berhasil diimport."

seed-ebook: generate-pdfs
	@echo "==> Mengupload berkas PDF sampel ke VPS dan container galura-slims-ebook..."
	rsync -avz -e "ssh -i $(shell grep DEPLOY_SSH_KEY .env | cut -d= -f2)" database/seeds/*.pdf $(shell grep DEPLOY_SSH_USER .env | cut -d= -f2)@$(shell grep DEPLOY_SSH_IP .env | cut -d= -f2):/tmp/slims_ebook_pdfs/
	ssh -i $(shell grep DEPLOY_SSH_KEY .env | cut -d= -f2) $(shell grep DEPLOY_SSH_USER .env | cut -d= -f2)@$(shell grep DEPLOY_SSH_IP .env | cut -d= -f2) \
		"sudo docker cp /tmp/slims_ebook_pdfs/. galura-slims-ebook:/var/www/html/repository/ && sudo docker exec -i galura-slims-ebook chown -R www-data:www-data /var/www/html/repository && sudo docker exec -i galura-slims-ebook chmod -R 775 /var/www/html/repository"
	@echo "==> Mengimport seed data metadata e-book ke senayan_ebook..."
	ssh -i $(shell grep DEPLOY_SSH_KEY .env | cut -d= -f2) $(shell grep DEPLOY_SSH_USER .env | cut -d= -f2)@$(shell grep DEPLOY_SSH_IP .env | cut -d= -f2) \
		"sudo docker exec -i galura-slims-ebook-db mariadb -u root -p'$(shell grep DB_PASS_EBOOK .env | cut -d= -f2)' senayan_ebook" < database/seeds/seed_ebook.sql
	@echo "==> [SUKSES] Berkas PDF dan seed metadata SLiMS EBOOK berhasil dipasang."

seed: seed-edu seed-ebook

