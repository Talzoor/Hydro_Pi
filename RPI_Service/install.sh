#!/bin/bash
# Script to create 'x' service

SERVICE_NAME = TEST.service
DESCRIPTION = TESTING
PYTHON_FILE = /home/pi/PythonScripts/Hydro_Pi/TEMP/Pi_switch/Pi_switch_main.py

cd /lib/systemd/system/
sudo sh -c 'echo "

[Unit]
Description=Hello World
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 "PYTHON_FILE ${!PYTHON_FILE}"
Restart=on-abort

[Install]
WantedBy=multi-user.target

" >> "SERVICE_NAME ${!SERVICE_NAME}"'
