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

# load custom commands from file to dictionary
def load_custom():
    try:
        custom = open("/etc/pi-btconf/custom_commands.txt")   # open custom commands file
        custom_text = custom.readlines()   # read custom commands into list of strings
        custom.close()   # close file
        command_dict = {}
        for num, line in enumerate(custom_text):   # for each line
            line_split = line.replace("\n", "").split(" = ")   # split string to list by " = "
            command_dict[line_split[0]] = line_split[1].replace('"', '')   # append split line to dictionary
        return custom_text, command_dict
    except:
        return [], {}

def run():
    subprocess.Popen("bluetoothctl power on", shell=True)   # turn on bluetooth
    subprocess.Popen("rfkill unblock bluetooth", shell=True)   # enable bluetooth
    bluetooth = Bluetooth()
    wlan = []
    set_wlan = "wlan0"   # default wlan interface
    set_network = 0
    custom_text, command_dict = load_custom()
    while True:
        command = bluetooth.receive()   # receive ssid from second device

        
        if command != "":   # if there is command
            bluetooth.clear_buffer()   # clear buffer
            
            if command == "terminal":
                bluetooth.send("pi-btconf will be disconnected" + "\n\r")
                bluetooth.send("Please open terminal emulator and connect to raspberry pi" + "\n\r")
                # restart bluetoothd in compatibility mode, otherwise sdptool wont work
                subprocess.Popen("rfkill block bluetooth", shell=True)
                subprocess.Popen("killall bluetoothd", shell=True)
                subprocess.Popen("bluetoothd -C &", shell=True)
                subprocess.Popen("rfkill unblock bluetooth", shell=True)
                # setup RFCOMM terminal
                subprocess.Popen("sudo sdptool add sp", shell=True)
                subprocess.Popen('sudo rfcomm -S -E -A watch rfcomm0 0 sh -c "setsid getty rfcomm0 115200" > /dev/null &', shell=True)
            
            if command == "list":
                wlan = []   # reset list of networks
                net_interfaces = os.listdir("/sys/class/net/")
                for net_interface in net_interfaces:
                    if "wireless" in os.listdir("/sys/class/net/" + net_interface):
                        wlan.append(net_interface)
                bluetooth.send("WLANs: " + str(wlan).replace("'", "").replace("[", "").replace("]", "") + "\n\r")
            
            if command.split(" ")[0] == "interface":
                if  len(command.split(" ")) >= 2:
                    wlan = []   # reset list of networks
                    net_interfaces = os.listdir("/sys/class/net/")
                    for net_interface in net_interfaces:   # get list of interfaces
                        if "wireless" in os.listdir("/sys/class/net/" + net_interface):
                            wlan.append(net_interface)
                    if command.split(" ")[1] in wlan:   # check if inputed interface exists
                        set_wlan = command.split(" ")[1]
                    else:
                        bluetooth.send("Invalid network interface" + "\n\r")
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command == "saved":
                proc = subprocess.Popen("wpa_cli -i "+set_wlan+" list_networks", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                bluetooth.send(proc[0].replace(b"\n", b"\n\r") + b"\n\r") 
            
            if command == "scan":
                subprocess.Popen("wpa_cli -i "+set_wlan+" scan", shell=True)
                proc = subprocess.Popen("wpa_cli -i "+set_wlan+" scan_results", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                bluetooth.send(proc[0].replace(b"\n", b"\n\r") + b"\n\r") 
            
            if command.split(" ")[0] == "network":
                if  len(command.split(" ")) == 2:   # if there is 2 words
                    set_wlan = command.split(" ")[1]   # get second word
                    bluetooth.send("Network interface set to:" + str(set_wlan) + "\n\r")   # return selected wlan
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command == "new":
                proc = subprocess.Popen("wpa_cli -i "+set_wlan+" add_network", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
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
                    subprocess.Popen("wpa_cli -i "+set_wlan+" set_network ssid "+set_ssid, shell=True)
                    bluetooth.send("UUID for network " + set_network + " set to:" + str(set_ssid) + "\r")   # return selected ssid
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "pass":
                if  len(command.split(" ")) >= 2:
                    password = command.split(" ")[1]
                    if password == "NONE_PASS":
                        subprocess.Popen("wpa_cli -i "+set_wlan+" set_network key_mgmt NONE", shell=True)
                        bluetooth.send("No password set for network " + set_network + "\r")   # return that password is set
                    else:
                        subprocess.Popen("wpa_cli -i "+set_wlan+" set_network psk "+password, shell=True)
                        bluetooth.send("Password set for network " + set_network + "\r")   # return that password is set
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "connect":
                if  len(command.split(" ")) >= 2:
                    conn_network = command.split(" ")[1]
                    subprocess.Popen("wpa_cli -i "+set_wlan+" enable_network "+conn_network, shell=True)
                    bluetooth.send("Connecting to network" + set_network + "\r")   # return that it start connecting
                else: 
                    bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "status":
                proc = subprocess.Popen("wpa_cli status", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                bluetooth.send(proc[0].replace(b"\n", b"\n\r") + b"\n\r") 
            
            if command == "ipa":
                hostname = socket.gethostname()   # find hostname
                ip = socket.gethostbyname(hostname + ".local")   # find IP address
                bluetooth.send("Local IP address:" + str(ip) + "\n\r")   # send IP address
            
            if command == "shutdown":
                bluetooth.send("The system will poweroff now!" + "\n\r")
                subprocess.Popen("shutdown now", shell=True)   # shutdown device
                
            if command == "reboot":
                bluetooth.send("The system will reboot now!" + "\n\r")
                subprocess.Popen("reboot", shell=True)   # reboot device
            
            if command == "state":
                for num, command in enumerate(interfaces_get):   # for all interfaces: get their state
                    proc = subprocess.Popen("raspi-config nonint "+command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    if proc[0].decode() == "0\n":   # if state is 0 (for some reason, it is inverted)
                        bluetooth.send(interface_names[num] + " is ON" + "\n\r")   # it is ON
                    else:  # if state is 1
                        bluetooth.send(interface_names[num] + " is OFF" + "\n\r")   # it is Off
             
            for num, interface in enumerate(interfaces):
                if command.split(" ")[0] == interface:
                    if  len(command.split(" ")) == 2:
                        if command.split(" ")[1] == "on":   # turn on interface
                            subprocess.Popen("raspi-config nonint "+interfaces_do[num]+"0", shell=True)
                            bluetooth.send(interface_names[num] + " turned ON" + "\n\r")
                        if command.split(" ")[1] == "off":   # turn off interface
                            subprocess.Popen("raspi-config nonint "+interfaces_do[num]+"1", shell=True)
                            bluetooth.send(interface_names[num] + " turned OFF" + "\n\r")
                    else:
                        bluetooth.send("Invalid input" + "\n\r")
            
            if command.split(" ")[0] == "boot":
                if  len(command.split(" ")) == 2:
                    if command.split(" ")[1] == "cli":   # boot to cli
                        subprocess.Popen("raspi-config nonint do_boot_behaviour B1", shell=True)
                        bluetooth.send("Next boot will be into CLI" + "\n\r")
                    if command.split(" ")[1] == "de":   # boot to desktop
                        subprocess.Popen("raspi-config nonint do_boot_behaviour B3", shell=True)
                        bluetooth.send("Next boot will be into Desktop" + "\n\r")
            
            if custom_text != []:
                if command == "custom":
                    if custom_text != []:
                        for line in custom_text:   # for each line
                            bluetooth.send(line + "\n\r")   # add newline and send it
                    else:
                        bluetooth.send("There are no available custom commands" + "\n\r")
                
                if command in command_dict.keys():
                    command_run = command_dict[command]   # get command from dictionary by name
                    proc = subprocess.Popen(command_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
                    bluetooth.send(proc[0].replace(b"\n", b"\n\r") + b"\n\r")   # return output if any
            
            if command == "help":
                bluetooth.send("terminal - Setup RFCOMM terminal" + "\n\r")
                bluetooth.send("list - List available WLAN interfaces" + "\n\r")
                bluetooth.send("interface <str> - Set WLAN interface" + "\n\r")
                bluetooth.send("saved - List saved networks" + "\n\r")
                bluetooth.send("scan - Scan for available networks" + "\n\r")
                bluetooth.send("new - Add new network to saved networks" + "\n\r")
                bluetooth.send("net <num> - Select network number to edit it" + "\n\r")
                bluetooth.send("ssid <str> - Set new network ssid" + "\n\r")
                bluetooth.send("pass <str> - Set new network password" + "\n\r")
                bluetooth.send("connect <num> - Connect to selected network" + "\n\r")
                bluetooth.send("status - Return connection status" + "\n\r")
                bluetooth.send("ipa - Show IP address" + "\n\r")
                bluetooth.send("shutdown - Shutdown device now" + "\n\r")
                bluetooth.send("reboot - Reboot device now" + "\n\r")
                bluetooth.send("state - Show interfaces state" + "\n\r")
                bluetooth.send("<interface> <on/off> - Enable / Disable interface" + "\n\r")
                bluetooth.send("boot <cli/de> - Boot into CLI / Desktop" + "\n\r")
                bluetooth.send("custom - List available custom commands" + "\n\r")
                bluetooth.send("quit - End session and disable bluetooth" + "\n\r")
                
            if command == "quit":
                break

    subprocess.Popen("rfkill block bluetooth", shell=True)   # disable bluetooth

run()

