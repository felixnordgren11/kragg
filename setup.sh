#! /usr/bin/bash/

#Move innit.sh to /etc/init.d/ and make it run at boot

/kragg/innit.sh
chmod +x innit-sh
sudo mv innit.sh /etc/init.d/
sudo update-rc.d innit.sh defaults

#install requirements

xargs sudo apt-get install /kragg/requirements.txt/

#replace the config file

sudo rm -f ./home/pi/boot/config.txt

/kragg/config.txt
chmod +x config.txt
sudo mv config.txt /home/pi/boot/


echo "Merry Dickmas Santa Cock" "Peter Piper picked a peck of pickled cocks"
