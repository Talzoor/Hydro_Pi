#!/bin/bash
# Script to create 'x' service

SERVICE_NAME="TEST.service"
DESCRIPTION ="TESTING"
PYTHON_FILE"="/home/pi/PythonScripts/Hydro_Pi/TEMP/Pi_switch/Pi_switch_main.py"

cd /lib/systemd/system/
sudo sh -c 'echo "\n\n[Unit]\nDescription=Hello World\nAfter=multi-user.target\n[Service]\nType=simple\nExecStart=/usr/bin/python3 "PYTHON_FILE ${!PYTHON_FILE}"\nRestart=on-abort\n[Install]\nWantedBy=multi-user.target\n\n" >> "SERVICE_NAME ${!SERVICE_NAME}"'
