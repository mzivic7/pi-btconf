#!/bin/bash

# uninstall packages and libs
sudo pip3 uninstall pybluez

# remove files and dirs
sudo rm /usr/local/sbin/pi-btconf.py
sudo rm /usr/local/sbin/pi-btconf-launcher.py
sudo rm /etc/systemd/system/pi-btconf.service
sudo rm -rf /etc/pi-btconf/

# stop and remove service
sudo systemctl stop pi-btconf.service
sudo systemctl disable pi-btconf.service

echo "pi-btconf service is sucsessfully removed." 

