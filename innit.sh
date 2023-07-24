#! /bin/bash
sudo ip link set can0 up type can bitrate 500000
git pull
chmod -x ~/kragg/innit.sh
python ~/kragg/main.py
