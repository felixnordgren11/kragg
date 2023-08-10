#! /bin/bash
cd ~/kragg
sudo ip link set can0 up type can bitrate 500000
chmod +x innit.sh
python main.py
