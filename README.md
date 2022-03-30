# Config over Bluetooth for Raspberry Pi
Python script used to configure Raspberry Pi wifi connections, toggle interfaces and many more.

## Installation
Open terminal in project folder and run `python3 pi-btconf.py`

## Usage
Pair raspberry pi with second device.
Run pi-btconf script, it will turn on bluetooth if it is off.
On second device any terminal that communicates over bluetooth RFCOMM protocol will work.
There are many apps designed for android bluetooth RFCOMM (like [rfterm](https://github.com/hxxr/rfterm)).

## Features:
 - List saved networks
 - Scan for available networks
 - Set WLAN interface
 - Add new network to saved networks
 - Set new network ssid and password
 - Connect to selected network
 - Show IP address
 - Shutdown or reboot device
 - Show interfaces state
 - Enable / Disable interfaces
 - Next boot into CLI / Desktop
 - End session and disable bluetooth
