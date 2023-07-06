#! /bin/bash

git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
# Ask for user input
read -p "Do you want to reboot the operating system? (y/n): " answer

# Check user input
if [[ "$answer" == "y" ]]; then
    # Running LCD35-show and rebooting the operating system
    echo "Rebooting the operating system..."
    sudo ./LCD35-show
elif [[ "$answer" == "n" ]]; then
    echo "Not rebooting the operating system."
else
    echo "Invalid input. Please enter either 'y' or 'n'."
fi