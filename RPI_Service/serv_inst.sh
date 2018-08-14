#!/bin/bash
# Created by Tal Zoor
# Script to create 'SERVICE_NAME' service
# fill in 4 variables -->

SERVICE_NAME="Pi_switch.service"
DESCRIPTION="Controling taps"
PYTHON_FILE="/home/pi/PythonScripts/Hydro_Pi/Pi_switch/Pi_switch_main.py"
SYS_SERVICE_DIR="/lib/systemd/system/"

# Start of script

rm "$SERVICE_NAME"

echo "$PWD"
echo "service name is :"$SERVICE_NAME""

echo " " >> "$SERVICE_NAME"

echo "[Unit]                                    "   >> "$SERVICE_NAME"
echo "Description="$DESCRIPTION"                "   >> "$SERVICE_NAME"
echo "After=multi-user.target                   "   >> "$SERVICE_NAME"

echo "                                          "   >> "$SERVICE_NAME"
echo "[Service]                                 "   >> "$SERVICE_NAME"
echo "Type=simple                               "   >> "$SERVICE_NAME"
echo "ExecStart=/usr/bin/python3 "$PYTHON_FILE" "   >> "$SERVICE_NAME"
echo "Restart=on-abort                          "   >> "$SERVICE_NAME"

echo "                                          "   >> "$SERVICE_NAME"
echo "[Install]                                 "   >> "$SERVICE_NAME"
echo "WantedBy=multi-user.target                "   >> "$SERVICE_NAME"

echo "----Created.----"

sudo cp "$SERVICE_NAME" "$SYS_SERVICE_DIR"

echo "----Copied to :"$SYS_SERVICE_DIR" ----"
