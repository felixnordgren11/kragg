#! /bin/bash
sudo ip link set can0 up type can bitrate 500000
git pull
python ~/kragg/main.py
