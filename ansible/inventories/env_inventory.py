#!/usr/bin/env python3
import json
import os
from pathlib import Path


def load_dotenv(path):
    values = {}
    if not path.exists():
        return values

    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value

    return values


repo_root = Path(__file__).resolve().parents[2]
dotenv = load_dotenv(repo_root / ".env")
deploy_keys = {
    "DEPLOY_IMAGE_REPO",
    "DEPLOY_IMAGE_TAG",
    "DEPLOY_DOCKER_NETWORK",
    "DEPLOY_PORT_EDU",
    "DEPLOY_CONTAINER_PORT_EDU",
    "DEPLOY_DB_PORT_EDU",
    "DEPLOY_IMAGE_EDU",
    "DEPLOY_PORT_EBOOK",
    "DEPLOY_CONTAINER_PORT_EBOOK",
    "DEPLOY_DB_PORT_EBOOK",
    "DEPLOY_IMAGE_EBOOK",
    "GHCR_USERNAME",
    "GHCR_TOKEN",
    "DB_USER",
    "DB_PASS",
}
deploy_env = {key: value for key, value in dotenv.items() if key in deploy_keys}


def env(name, default=""):
    return os.environ.get(name) or dotenv.get(name) or default


host = env("DEPLOY_SSH_IP", "43.159.63.105")
user = env("DEPLOY_SSH_USER", "ubuntu")
key = env("DEPLOY_SSH_KEY", "/Users/admin/.ssh/vps_baru.key")

if not host:
    inventory = {"_meta": {"hostvars": {}}}
else:
    hostvars = {
        "deploy_target": {
            "ansible_host": host,
            "ansible_user": user,
            "ansible_ssh_private_key_file": key,
            "ansible_python_interpreter": "/usr/bin/python3",
            "deploy_env": deploy_env,
        }
    }

    inventory = {
        "all": {"children": ["webservers"]},
        "webservers": {"hosts": ["deploy_target"]},
        "_meta": {"hostvars": hostvars},
    }

print(json.dumps(inventory))
