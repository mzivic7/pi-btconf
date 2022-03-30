#!/usr/bin/python3

import os
import subprocess
import bluetooth
import socket  

interfaces_get = ("get_ssh", "get_vnc", "get_spi", "get_i2c", "get_onewire", "get_rgpio", "get_boot_cli")
interfaces_do = ("do_ssh", "do_vnc", "do_spi", "do_i2c", "do_onewire", "do_rgpio")
interface_names = ("SSH", "VNC", "SPI", "I2C", "1Wire", "RGPIO", "boot cli")
interfaces = ("ssh", "vnc", "spi", "i2c", "1wire", "rgpio")   # boot cli has different commands

class Bluetooth:
    def __init__(self):
        self.server = bluetooth.BluetoothSocket( bluetooth.RFCOMM )   # start RFCOMM
        port = 1   # tcp port
        self.server.bind(("",port))   # bind tcp connection
        self.server.listen(1)   # listen on port 1
        self.client, address = self.server.accept()   # accept connection
        self.buffer = b""   # buffer to store character
        
    # receiving data
    def receive(self):
        data = self.client.recv(1024)
        self.client.send(data)   # send back data to show it
        if len(data): # if there is data
            if data != b'\n':
                self.buffer += data
            else:
                self.client.send(b"\r")   # go to start of newline
                if len(self.buffer): # if there is data in buffer
                    return self.buffer.decode()   # return data
                else: # if not:
                    return "" # return nothing
        return ""

    
    # sending data
    def send(self, data):
        self.client.send(data)
    
    # clear buffer after it is outputted
    def clear_buffer(self):
        self.buffer = b""

def run():
    subprocess.Popen(["rfkill", "unblock", "bluetooth"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)   # enable bluetooth
    bluetooth = Bluetooth()
    wlan = []
    set_wlan = "wlan0" ###
    set_network = 0
    while True:
        command = bluetooth.receive()   # receive ssid from second device

        
        if command != "":   # if there is command
            bluetooth.clear_buffer()   # clear buffer
            
            if command == "list":
                wlan = []   # reset list of networks
                net_interfaces = os.listdir("/sys/class/net/")
                for net_interface in net_interfaces:
                    if "wireless" in os.listdir("/sys/class/net/" + net_interface):
                        wlan.append(net_interface)
                bluetooth.send("WLANs: " + str(wlan).replace("'", "").replace("[", "").replace("]", "") + "\n\r")
            
            if command == "saved":
            	proc = subprocess.Popen(["wpa_cli", "-i", set_wlan, "list_networks"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
            	bluetooth.send(proc[0].replace(b"\n", b"\n\r") + b"\n\r") 
            
            if command == "scan":
                subprocess.Popen(["wpa_cli", "-i", set_wlan, "scan"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                proc = subprocess.Popen(["wpa_cli", "-i", set_wlan, "scan_results"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
                bluetooth.send(proc[0].replace(b"\n", b"\n\r") + b"\n\r") 
            
            if command.split(" ")[0] == "network":
                if  len(command.split(" ")) == 2:   # if there is 2 words
                    set_wlan = command.split(" ")[1]   # get second word
                    bluetooth.send("Network interface set to:" + str(set_wlan) + "\n\r")   # return selected wlan
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command == "new":
            	proc = subprocess.Popen(["wpa_cli", "-i", set_wlan, "add_network"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
            	bluetooth.send("Added new network, number:", str(proc)) 
            
            if command.split(" ")[0] == "net":
                if  len(command.split(" ")) == 2:
                    set_network = command.split(" ")[1]
                    bluetooth.send("Selected network number " + set_network + "\n\r")
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "ssid":
                if  len(command.split(" ")) >= 2:
                    set_ssid = command.split(" ")[1]
                    subprocess.Popen(["wpa_cli", "-i", set_wlan, "set_network",  "ssid", set_ssid], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    bluetooth.send("UUID for network " + set_network + " set to:" + str(set_ssid) + "\r")   # return selected ssid
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "pass":
                if  len(command.split(" ")) >= 2:
                    password = command.split(" ")[1]
                    if password == "NONE_PASS":
                        subprocess.Popen(["wpa_cli", "-i", set_wlan, "set_network",  "key_mgmt", "NONE"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        bluetooth.send("No password set for network " + set_network + "\r")   # return that password is set
                    else:
                        subprocess.Popen(["wpa_cli", "-i", set_wlan, "set_network",  "psk", password], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        bluetooth.send("Password set for network " + set_network + "\r")   # return that password is set
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "connect":
                if  len(command.split(" ")) >= 2:
                    conn_network = command.split(" ")[1]
                    subprocess.Popen(["wpa_cli", "-i", set_wlan, "enable_network", conn_network], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    bluetooth.send("Connecting to network" + set_network + "\r")   # return that it start connecting
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
                
            
            if command == "ipa":
                hostname = socket.gethostname()   # find hostname
                ip = socket.gethostbyname(hostname + ".local")   # find IP address
                bluetooth.send("Local IP address:" + str(ip) + "\n\r")   # send IP address
            
            if command == "shutdown":
                bluetooth.send("Full shutdown" + "\n\r")
                subprocess.Popen(["shutdown now"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)   # shutdown device
                
            if command == "reboot":
                bluetooth.send("Rebooting" + "\n\r")
                subprocess.Popen(["reboot"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)   # reboot device
            
            if command == "state":
                for num, command in enumerate(interfaces_get):   # for all interfaces: get theit state
                    proc = subprocess.Popen(["raspi-config", "nonint",  command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()
                    if proc[0].decode() == "0\n":   # if state is 0 (for some reason, it is inverted)
                        bluetooth.send(interface_names[num] + " is ON" + "\n\r")   # it is ON
                    else:  # if state is 1
                        bluetooth.send(interface_names[num] + " is OFF" + "\n\r")   # it is Off
             
            for num, interface in enumerate(interfaces):
                if command.split(" ")[0] == interface:
                    if  len(command.split(" ")) == 2:
                        if command.split(" ")[1] == "on":   # turn on interface
                            subprocess.Popen(["raspi-config", "nonint", interfaces_do[num], "0"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                            bluetooth.send(interface_names[num] + " turned ON" + "\n\r")
                        if command.split(" ")[1] == "off":   # turn off interface
                            subprocess.Popen(["raspi-config", "nonint", interfaces_do[num], "1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                            bluetooth.send(interface_names[num] + " turned OFF" + "\n\r")
                    else:
                        bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "boot":
                if  len(command.split(" ")) == 2:
                    if command.split(" ")[1] == "cli":   # boot to cli
                        subprocess.Popen(["raspi-config", "nonint", "do_boot_behaviour", "B1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        bluetooth.send("Next boot wil be into CLI" + "\n\r")
                    if command.split(" ")[1] == "de":   # boot to desktop
                        subprocess.Popen(["raspi-config", "nonint", "do_boot_behaviour", "B3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                        bluetooth.send("Next boot wil be into Desktop" + "\n\r")
            
            if command == "help":
                bluetooth.send("list - List available WLAN interfaces" + "\n\r")
                bluetooth.send("saved - List saved networks" + "\n\r")
                bluetooth.send("scan - Scan for available networks" + "\n\r")
                bluetooth.send("wlan <str> - Set WLAN interface" + "\n\r")
                bluetooth.send("new - Add new network to saved networks" + "\n\r")
                bluetooth.send("net <num> - Select network number to edit it" + "\n\r")
                bluetooth.send("ssid <str> - Set new network ssid" + "\n\r")
                bluetooth.send("pass <str> - Set new network password" + "\n\r")
                bluetooth.send("connect <num> - Connect to selected network" + "\n\r")
                bluetooth.send("ipa - Show IP address" + "\n\r")
                bluetooth.send("shutdown - Shutdown device now" + "\n\r")
                bluetooth.send("reboot - Reboot device" + "\n\r")
                bluetooth.send("state - Show interfaces state" + "\n\r")
                bluetooth.send("<interface> <on/off> - Enable / Disable interface" + "\n\r")
                bluetooth.send("boot <cli/de> - Boot into CLI / Desktop" + "\n\r")
                bluetooth.send("quit - End session and disable bluetooth" + "\n\r")
                
            if command == "quit":
                break

    subprocess.Popen(["rfkill", "block", "bluetooth"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)   # disable bluetooth

run()

