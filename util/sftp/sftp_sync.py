#!/usr/bin/env python3
"""Sync SFTP remote folders to local directories, driven by a YAML config file."""

import argparse
import logging
import os
import stat
import sys

import yaml
import paramiko

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("sftp_sync")


def load_config(path = 'config.yml'):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def connect(host_cfg):
    transport = paramiko.Transport((host_cfg["host"], host_cfg.get("port", 22)))
    key_path = host_cfg.get("private_key")
    if key_path:
        pkey = paramiko.RSAKey.from_private_key_file(
            os.path.expanduser(key_path), password=host_cfg.get("private_key_passphrase")
        )
        transport.connect(username=host_cfg["username"], pkey=pkey)
    else:
        transport.connect(username=host_cfg["username"], password=host_cfg["password"])
    return transport, paramiko.SFTPClient.from_transport(transport)


def remote_file_is_newer(sftp, remote_path, local_path):
    if not os.path.exists(local_path):
        return True
    remote_mtime = sftp.stat(remote_path).st_mtime
    local_mtime = os.path.getmtime(local_path)
    return remote_mtime > local_mtime


def sync_dir(sftp, remote_dir, local_dir, dry_run=False):
    os.makedirs(local_dir, exist_ok=True)

    for entry in sftp.listdir_attr(remote_dir):
        remote_path = f"{remote_dir}/{entry.filename}"
        local_path = os.path.join(local_dir, entry.filename)

        if stat.S_ISDIR(entry.st_mode):
            sync_dir(sftp, remote_path, local_path, dry_run=dry_run)
        else:
            if remote_file_is_newer(sftp, remote_path, local_path):
                if dry_run:
                    log.info("Would download: %s -> %s", remote_path, local_path)
                else:
                    log.info("Downloading: %s -> %s", remote_path, local_path)
                    sftp.get(remote_path, local_path)
            else:
                log.debug("Skipping up-to-date file: %s", local_path)


def main():
    parser = argparse.ArgumentParser(description="Sync SFTP remote folders to local directories.")
    parser.add_argument("--dry-run", action="store_true", help="List actions without downloading files")
    args = parser.parse_args()

    config = load_config()
    dry_run = args.dry_run

    for host_cfg in config["hosts"]:
        log.info("Connecting to %s@%s", host_cfg["username"], host_cfg["host"])
        try:
            transport, sftp = connect(host_cfg)
        except Exception as exc:
            log.error("Failed to connect to %s: %s", host_cfg["host"], exc)
            continue

        try:
            for folder in host_cfg["folders"]:
                remote_dir = folder["remote"]
                local_base = os.path.expanduser(folder["local"])
                local_dir = os.path.join(local_base, os.path.basename(remote_dir.rstrip("/")))
                log.info("Syncing %s -> %s", remote_dir, local_dir)
                try:
                    sync_dir(sftp, remote_dir, local_dir, dry_run = dry_run)
                except Exception as exc:
                    log.error("Failed to sync %s: %s", remote_dir, exc)
        finally:
            sftp.close()
            transport.close()


if __name__ == "__main__":
    sys.exit(main())
