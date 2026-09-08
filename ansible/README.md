# Ansible Provisioning & Deployment for Galura SLiMS

Panduan Ansible untuk deployment dan manajemen infrastruktur 2 sub-domain SLiMS di VPS:
- **`slims-edu.galura.id`** (Kontainer: `galura-slims-edu`, Port App: `8081`, Port DB: `3307`)
- **`slims-ebook.galura.id`** (Kontainer: `galura-slims-ebook`, Port App: `8082`, Port DB: `3308`)

---

## Struktur Folder

```text
ansible/
├── ansible.cfg
├── README.md
├── inventories/
│   ├── env_inventory.py         # Dynamic inventory reading .env
│   ├── production/
│   │   ├── hosts.ini            # Static production hosts
│   │   └── group_vars/
│   └── staging/
│       └── hosts.ini
├── playbooks/
│   ├── site.yml                 # Full server setup (docker, firewall, nginx, app)
│   ├── deploy-app.yml           # Container deployment per zone (edu, ebook, all)
│   └── deploy-local-build.yml   # VPS source code build & deployment
└── roles/
    ├── docker/                  # Docker Engine setup
    ├── firewall/                # UFW Firewall setup
    ├── nginx/                   # Nginx reverse proxy setup (vhost.j2)
    └── app/                     # SLiMS & MariaDB container setup
```

---

## Konfigurasi Credential (.env)

Atur variabel environment di `.env` root repository:

```env
DEPLOY_SSH_IP=43.159.63.105
DEPLOY_SSH_USER=ubuntu
DEPLOY_SSH_KEY=/Users/admin/.ssh/vps_baru.key
DEPLOY_IMAGE_REPO=ghcr.io/galura-it-solution/galura-slims
GHCR_USERNAME=galura-it-solution
GHCR_TOKEN=your_token_here
```

---

## Perintah Utama Deployment (Make Commands)

### 1. Test Koneksi VPS
```bash
make deploy-ping
```

### 2. Validasi Syntax Playbook
```bash
make deploy-syntax-check
```

### 3. Full Provisioning (Server Baru)
```bash
ansible-playbook -i ansible/inventories/production/hosts.ini ansible/playbooks/site.yml
```

### 4. Deploy Zone Tertentu
- **Deploy `slims-edu.galura.id`**:
  ```bash
  make deploy-zone ZONE=edu
  ```

- **Deploy `slims-ebook.galura.id`**:
  ```bash
  make deploy-zone ZONE=ebook
  ```

- **Deploy Semua Zone (`edu` & `ebook`)**:
  ```bash
  make deploy
  ```
