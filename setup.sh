#! /bin/bash

#Move innit.sh to /etc/init.d/ and make it run at boot
chmod +x innit.sh
sudo mv innit.sh /etc/init.d/
sudo update-rc.d innit.sh defaults

#install requirements

pip install -r requirements.txt

#replace the config file

sudo rm -f /home/pi/boot/config.txt
#chmod +x config.txt
sudo mv config.txt /home/pi/boot

#Clone the Git repository and run the file enabling the LCD screen

git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
echo "Enter 1 to reboot"
read in
test $in -eq 1 && sudo ./LCD35-show