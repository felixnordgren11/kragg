#! /usr/bin/bash/

#Move innit.sh to /etc/init.d/ and make it run at boot

git clone https://github.com/goodtft/LCD-show.git
chmod -r 755 LCD-show
cd LCD-show/
sudo ./LCD35-show
sudo ./LCD-hdmi
sleep 5
cd ..

/kragg/innit.sh

chmod +x innit.sh
sudo mv innit.sh /etc/init.d/
sudo update-rc.d innit.sh defaults

#install requirements

pip install -r requirements.txt

#replace the config file

sudo rm -f ./home/pi/boot/config.txt

/kragg/config.txt
chmod +x config.txt
sudo mv config.txt /home/pi/boot/


echo "Enter 1 to reboot"
read in
test $in -eq 1 && sudo reboot