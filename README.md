# Config over Bluetooth for Raspberry Pi
Python script used to configure Raspberry Pi wifi connections, toggle interfaces and much more.

## Installation
To install, run following commands:
```
git clone https://github.com/mzivic7/py-btconf
sudo pi-btconf/install.sh
```
This will install all dependancies and configure service that waits for button double-press.

## Usage
Pair raspberry pi with second device.
Connect button to GPIO pin 3 and gnd.
To start pi-btconf, push button twice under 0.5 seconds. This will also terminate pi-btconf if it is previously started and turn off bluetooth.
Pi-btconf will turn on bluetooth if it is off.

On second device any terminal that communicates over bluetooth RFCOMM protocol will work.
There are many apps designed for android bluetooth RFCOMM (like [BlueTerm](https://play.google.com/store/apps/details?id=es.pymasde.blueterm)).

## Features:
 - Swich on / off script and bluetooth on button double-press
 - Setup terminal over bluetooth RFCOMM
 - List saved networks
 - Scan for available networks
 - Set WLAN interface
 - Add new network to saved networks
 - Set new network ssid and password
 - Connect to selected network and show network status
 - Show IP address
 - Shutdown or reboot device
 - Show interfaces state
 - Enable / Disable interfaces
 - Next boot into CLI / Desktop
 - Run pre-set custom command in terminal
 - End session and disable bluetooth

## Terminal:

Terminal function will work with any RFCOMM terminal on second device. 
On android, BlueTerm will work, but it may lack some important functons, like special keys and colors. (better: [rfterm](https://github.com/hxxr/rfterm)).  
When terminal is activated pi-btconf won't be able to connect.  
Pressing button twice will turn off bluetooth and disconnect terminal.

## Custom Commands:
Custom commands can be configured in: /etc/pi-btconf/custom_comands.txt  
Format:  
name = "command to run in terminal"  
Each line represents one command.  
There must be " = " separator and command must be inside "".
