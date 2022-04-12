#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

echo $SCRIPT_DIR
cp $SCRIPT_DIR/systemd/dawimond.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable dawimond
sudo systemctl start dawimond
