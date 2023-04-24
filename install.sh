#!/bin/bash

set -e # exit script immediately on error

PACKAGE_NAME="gacd_server"
SYSTEMD_CONFIG="/etc/systemd/system/${PACKAGE_NAME}.service"
SYMLINK = "/usr/local/bin/${PACKAGE_NAME}"

if [[ $UID != 0 ]]; then
    echo "Please run installation script with sudo"
    echo "Usage: sudo $0 $*"
    exit 1
fi

pip install .

echo "GitHub Actions CD server (${PACKAGE_NAME}) installed successfully. Daemon creating..."

touch $SYSTEMD_CONFIG

echo -e "[Unit]" >> $SYSTEMD_CONFIG
echo -e "Description=CD server for Neokaidan Github Actions pipeline" >> $SYSTEMD_CONFIG
echo -e "After=network-online.target" >> $SYSTEMD_CONFIG
echo -e "" >> $SYSTEMD_CONFIG
echo -e "[Service]" >> $SYSTEMD_CONFIG
echo -e "Type=simple" >> $SYSTEMD_CONFIG
echo -e "RestartSec=3" >> $SYSTEMD_CONFIG
echo -e "ExecStart=${SYMLINK}" >> $SYSTEMD_CONFIG
echo -e "" >> $SYSTEMD_CONFIG
echo -e "[Install]" >> $SYSTEMD_CONFIG
echo -e "WantedBy=multi-user.target" >> $SYSTEMD_CONFIG

systemctl daemon-reload
systemctl start ${PACKAGE_NAME}

echo "Github Action CD server daemon was installed successfully"
