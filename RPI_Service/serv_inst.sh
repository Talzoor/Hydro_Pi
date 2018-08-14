#!/bin/bash
# Script to create 'x' service

SERVICE_NAME="TEST.service"
DESCRIPTION="TESTING"
PYTHON_FILE"="/home/pi/PythonScripts/Hydro_Pi/TEMP/Pi_switch/Pi_switch_main.py"

cd /lib/systemd/system/
sudo sh -c 'echo " " >> "$SERVICE_NAME"'
sudo sh -c 'echo "[Unit]" >> "$SERVICE_NAME"'

sudo sh -c 'echo "[Unit]                        "   >> "$SERVICE_NAME"'
sudo sh -c 'echo "Description="$DESCRIPTION"    "   >> "$SERVICE_NAME"'
sudo sh -c 'echo "After=multi-user.target       "   >> "$SERVICE_NAME"'
sudo sh -c 'echo "[Service]                     " >> "$SERVICE_NAME"'
sudo sh -c 'echo "Type=simple                   " >> "$SERVICE_NAME"'
sudo sh -c 'echo "ExecStart=/usr/bin/python3 "PYTHON_FILE ${!PYTHON_FILE}"  " >> "$SERVICE_NAME"'
sudo sh -c 'echo "Restart=on-abort              " >> "$SERVICE_NAME"'
sudo sh -c 'echo "[Install]                     " >> "$SERVICE_NAME"'
sudo sh -c "echo "WantedBy=multi-user.target    " >> "$SERVICE_NAME""