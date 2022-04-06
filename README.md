# Config over Bluetooth for Raspberry Pi
Python script used to configure Raspberry Pi wifi connections, toggle interfaces and many more.

## Installation
To install run following commands:
```git clone https://github.com/mzivic7/py-btconf
sudo pi-btconf/install.sh```
This will install all dependancies and configure service that waits for button double-press.

## Usage
Pair raspberry pi with second device.
Connect button to GPIO pin 3 and gnd.
To start pi-btconf, push button twice under 0.5 seconds. This will also terminate pi-btconf if it is previously started.
Pi-btconf will turn on bluetooth if it is off.

On second device any terminal that communicates over bluetooth RFCOMM protocol will work.
There are many apps designed for android bluetooth RFCOMM (like [BlueTerm](https://play.google.com/store/apps/details?id=es.pymasde.blueterm)).
"terminal" function will work only with suitable terminal emulator on second device (for android, advised: [rfterm](https://github.com/hxxr/rfterm)) 

## Features:
 - Swich on / off script and bluetooth on button bouble-press
 - Run terminal
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
