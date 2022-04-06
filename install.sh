#!/bin/bash

# install packages and libs
sudo apt install bluetooth bluez python-bluetooth libbluetooth-dev
sudo pip3 install pybluez

# install files
sudo cp pi-btconf/pi-btconf.py /usr/local/sbin/pi-btconf.py
sudo cp pi-btconf/pi-btconf-launcher.py /usr/local/sbin/pi-btconf-launcher.py
sudo cp pi-btconf/pi-btconf.service /etc/systemd/system/pi-btconf.service
sudo chmod 755 /usr/local/sbin/pi-btconf-launcher.py
sudo chmod 755 /usr/local/sbin/pi-btconf.py
sudo chmod 644 /etc/systemd/system/pi-btconf.service
sudo chown root:root /etc/systemd/system/pi-btconf.service /usr/local/sbin/pi-btconf*

# start service
sudo systemctl enable pi-btconf.service
sudo systemctl start pi-btconf.service

echo "pi-btnap service is enabled and started." 
echo "Please reboot rpi, connect button to gpio pin 3 and ground, and have rpi and second device paired."
echo "To activate pi-btconf quickly push button twice. On second device open bluetooth RFCOMM terminal and connect to rpi."

