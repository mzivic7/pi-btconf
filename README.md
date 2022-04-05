# Config over Bluetooth for Raspberry Pi
Python script used to configure Raspberry Pi wifi connections, toggle interfaces and many more.

## Installation
To install run following commands:
`git clone https://github.com/mzivic7/py-btconf
sudo pi-btconf/install.sh`

## Usage
Pair raspberry pi with second device.
Run pi-btconf script, it will turn on bluetooth if it is off.
On second device any terminal that communicates over bluetooth RFCOMM protocol will work.
There are many apps designed for android bluetooth RFCOMM (like [BlueTerm](https://play.google.com/store/apps/details?id=es.pymasde.blueterm)).

To run script on button double-press, connect button to GPIO pin 3 and gnd.
Run button_launcher.py script in terminal.
To start pi-btconf, push button twice under 0.5 seconds. This will also terminate pi-btconf if it is previously started.

## Features:
 - Swich on / off script and bluetooth on button bouble-press
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
