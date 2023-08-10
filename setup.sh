#! /bin/bash

#Move innit.sh to /etc/init.d/ and make it run at boot


###chmod +x innit.sh
###sudo mv innit.sh /etc/init.d/
###sudo update-rc.d innit.sh defaults

#use chish.service to execute this instead
sudo mv chish.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/chish.service
sudo systemctl enable chish
sudo systemctl start chish


#install requirements

pip install -r requirements.txt

# For sound.
sudo apt-get install libsdl2-mixer-2.0-0

#replace the config file

sudo rm -f /home/pi/boot/config.txt
#chmod +x config.txt
sudo mv config.txt /home/pi/boot


#Run innit.sh at boot
mkdir /home/pi/.config/autostart
sudo mv /home/pi/kragg/startup.dekstop /home/pi/.config/autostart

# Check user input
if [[ "$answer" == "y" ]]; then
    # Running LCD35-show and rebooting the operating system
    echo "Rebooting the operating system..."
    sudo reboot
elif [[ "$answer" == "n" ]]; then
    echo "Not rebooting the operating system."
else
    echo "Invalid input. Please enter either 'y' or 'n'."
fi
