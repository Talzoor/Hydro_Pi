#!/bin/bash
# Created by Tal Zoor
# Script to create 'SERVICE_NAME' service
# fill in 4 (or just first 3) variables -->

SERVICE_NAME="Pi_switch.service"
DESCRIPTION="Controling taps"
PYTHON_FILE="/home/pi/PycharmProjects/Hydro_Pi/run.py"
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

sudo chmod 644 ""$SYS_SERVICE_DIR""$SERVICE_NAME""
chmod +x "$PYTHON_FILE"
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"