# 485 Lab PS
This repository contains code and instructions of how to convert the 485 AC-DC converter into a configurable lab bench power supply.

## Table of contents
* [General info](#general-info)
* [Hardware and Technologies](*hardware-and-technologies)
* [Setup](#setup)

## General info

This was a project to convert a AC-DC converter to a lab bench power supply unit. It utilizes a Raspberry Pi with a display which runs the GUI. It sends the users input to the 485 via CAN protocol. 

## Hardware and Technologies
The hardware needed for this project is:

* A Raspberry Pi 4/3 (or Zero if it could work)
* A 16 GB SD card
* A SPI-CAN extension, like this [one](https://www.electrokit.com/produkt/can-bus-modul-mcp2515-tja1050-spi/).
* [This LCD](https://www.electrokit.com/produkt/3-5-tft-display-for-raspberry-pi-med-touch/).
* One rotary encoder.
* Four buttons.
* Six 10kΩ resistors.
* The box which can be printed from the included STL-files.

The needed software:
* Python 3.10 and the dependencies listed in 'requirements.txt'
* A copy of Raspbian available from the [Raspberry Pi imager](https://www.raspberrypi.com/software/)

* ('python3 -m pip install --upgrade' Pillow to install latest Pillow version if requirements does not do this.)

## Setup

Begin by downloading the Raspberry Pi imager from the software page on their website. Then, insert the SD card into your computer and choose the 32-bit OS and write it to the SD. 

Now, insert the SD-card into the Raspberry PI and hook it up to a monitor in order to configure it. Choose a password and use *pi* as username. 

After it has been set up correctly, open the terminal and write:
```shell
git clone https://github.com/felixnordgren11/kragg
```
This will clone the repository into /home/pi.
Then you will have to type in the following commands:

```shell
cd kragg

chmod +x lcd.sh

./lcd.sh
```
Respond with a 'y' and then press enter when prompted, this will run the last file and reboot the system.
#
When the system has booted up again, open the terminal type in:
```shell
cd kragg

chmod +x setup.sh

./setup.sh
```
to enter the kragg folder, make the setup.sh file executable and then run it. When told, enter 1 and press 'Enter' to run the last file and reboot the system.



## Build

![alt text](https://github.com/felixnordgren11/kragg/dickmas.jpg?raw=true)


