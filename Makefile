SHELL := /bin/bash

ANSIBLE_DIR := ansible
ANSIBLE_INVENTORY := $(ANSIBLE_DIR)/inventories/env_inventory.py
ANSIBLE_DEPLOY_PLAYBOOK := $(ANSIBLE_DIR)/playbooks/deploy-app.yml
ANSIBLE_LOCAL_TEMP ?= /tmp/ansible-local-tmp
ANSIBLE_ENV := ANSIBLE_LOCAL_TEMP=$(ANSIBLE_LOCAL_TEMP) ANSIBLE_HOST_KEY_CHECKING=False ANSIBLE_CONFIG=$(ANSIBLE_DIR)/ansible.cfg

ZONE ?= all
TAG ?= latest
DEPLOY_EXTRA_VARS = deploy_zone=$(ZONE) deploy_image_tag=$(TAG)

.PHONY: help deploy deploy-zone deploy-edu deploy-ebook deploy-ping deploy-syntax-check docker-build-push-zone docker-build-push-all

help:
	@printf "Galura SLiMS Ansible Deployment Commands\n\n"
	@printf "  make deploy-ping                    Test koneksi SSH VPS dari .env\n"
	@printf "  make deploy-syntax-check            Validasi syntax Ansible Playbook\n"
	@printf "  make deploy                         Deploy semua zone (edu & ebook)\n"
	@printf "  make deploy-zone ZONE=edu           Deploy zone edu (slims-edu.galura.id)\n"
	@printf "  make deploy-zone ZONE=ebook         Deploy zone ebook (slims-ebook.galura.id)\n"
	@printf "  make deploy-edu                     Shortcut deploy zone edu\n"
	@printf "  make deploy-ebook                   Shortcut deploy zone ebook\n"

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
