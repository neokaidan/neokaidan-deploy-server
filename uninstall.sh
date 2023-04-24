#!/bin/bash

set -e # exit script immediately on error

PACKAGE_NAME="gacd_server"
SYSTEMD_CONFIG="/etc/systemd/system/${PACKAGE_NAME}.service"
SYSTEMD_CONFIG_MULTIUSER="/etc/systemd/system/multi-user.target/${PACKAGE_NAME}.service"

if [[ $UID != 0 ]]; then
    echo "Please run installation script with sudo"
    echo "Usage: sudo $0 $*"
    exit 1
fi

echo "Stopping daemon..."
systemctl stop ${PACKAGE_NAME}

echo "Uninstalling via pip..."
pip uninstall ${PACKAGE_NAME}

echo "GitHub Actions CD server (${PACKAGE_NAME}) uninstalled successfully. Daemon removing..."

rm -rf $SYSTEMD_CONFIG
rm -rf $SYSTEMD_CONFIG_MULTIUSER

systemctl daemon-reload

echo "Github Action CD server daemon was removed successfully"
