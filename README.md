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

* A Raspberry Pi 4/3 or Zero with 32-bit Rasbian.
* A SPI-CAN extension, like this [one](https://www.electrokit.com/produkt/can-bus-modul-mcp2515-tja1050-spi/).
* [This LCD](https://www.electrokit.com/produkt/3-5-tft-display-for-raspberry-pi-med-touch/).
* One rotary encoder.
* Four buttons.
* Six 10kΩ resistors.
* The box which can be printed from the included STL-files.

The needed software:
* Python 3.10 and the dependencies listed in 'requirements.txt'
*