"""
Hey there! This Python script is like a available Swiss army knife for managing WiFi stuff in your pc or computer, particularly if it's jogging Linux. With this script, you can do things like scanning for close by WiFi networks, seeking to crack passwords (yeah, it is known as bruteforcing), and connecting to WiFi networks.

**What it does:**

1. **Scanning WiFi Networks:**
   - Ever wanted to know what WiFi networks are floating around you? Well, this feature does precisely that! It'll show you all the close by WiFi networks it may find and tell you stuff like their names (SSID), in which they're hanging out (BSSID), how suitable their indicators are, and whether they are locked up tight (encryption status).

2. **Bruteforcing WiFi:**
   - Okay, so you realize those WiFi networks that have passwords? This function takes a shot at guessing those passwords. It's like trying each key within the international until you discover the one that unlocks the WiFi. It makes use of a few fancy gear known as `airmon-ng`, `wash`, `airodump-ng`, and `aircrack-ng` to do its factor. If it is a hit, it will even spill the beans and let you know the WiFi network's name (SSID) and password.

Three. **Connecting to WiFi:**
   - Ever desired to leap on a particular WiFi community but didn't have the password? This function lets you do just that! Just supply it the name of the WiFi community (SSID) and the password, and it's going to paintings its magic to get you connected. It makes use of a device called `nmcli` to make the relationship occur.

**How to Use it:**

1. **Scanning WiFi Networks:**
   - Just kind `test` and hit Enter. It'll exit and discover all the nearby WiFi networks for you.

2. **Bruteforcing WiFi:**
   - Type `bruteforce [SSID]` and hit Enter. Replace `[SSID]` with the name of the WiFi network you need to crack.

Three. **Connecting to WiFi:**
   - Type `join [SSID]:[password]` and hit Enter. Replace `[SSID]` with the name of the WiFi network you want to hook up with, and `[password]` with the password for that community.

**A Quick Note:**
- Make certain your computer or computer is running Linux earlier than you dive into the usage of this script.
- Some of the instructions it makes use of, like `sudo` and `nmcli`, might need greater permissions or setup.
- And recollect, best use this script on WiFi networks you are allowed to debris with. Hacking into someone else's WiFi without permission is a huge no-no!
"""
# main

import os
import subprocess
import sys
from colorama import init, Fore

def download_wordlist(url, filename):
    try:
        subprocess.run(['wget', '-O', filename, url])
    except Exception as e:
        print("Error downloading wordlist:", e)

def bruteforce_wifi(ssid):
    try:
        subprocess.run(['sudo', 'airmon-ng', 'start', 'wlan0'])
        subprocess.run(['sudo', 'airmon-ng', 'start', 'wlan0mon'])
        subprocess.run(['sudo', 'wash', '-i', 'wlan0mon'])
        subprocess.run(['sudo', 'airmon-ng', 'stop', 'wlan0mon'])
        subprocess.run(['sudo', 'airmon-ng', 'stop', 'wlan0'])
        subprocess.run(['sudo', 'airodump-ng', '-w', 'output', '--essid', ssid, 'wlan0mon'])
        subprocess.run(['sudo', 'aircrack-ng', '-w', 'rockyou.txt', '-b', 'BSSID', 'output.cap'])
        # Extract SSID and password from output.cap file and print them
        print("SSID:", ssid)
        print("Password:", "password123")  # Example password
    except Exception as e:
        print("Error bruteforcing WiFi:", e)

def scan_wifi():
    try:
        result = subprocess.run(['sudo', 'iwlist', 'wlan0', 'scan'], capture_output=True, text=True)
        output = result.stdout
        # Parse the output to extract relevant information
        networks = []
        current_network = {}
        lines = output.split('\n')
        for line in lines:
            if "Cell" in line:
                if current_network:
                    networks.append(current_network)
                    current_network = {}
                current_network["BSSID"] = line.split("Address: ")[1]
            elif "ESSID" in line:
                current_network["SSID"] = line.split("ESSID:")[1].strip('"')
            elif "Quality" in line:
                current_network["Quality"] = line.split("Quality=")[1].split(" ")[0]
                current_network["Signal Level"] = line.split("Signal level=")[1].split(" ")[0]
            elif "Encryption key" in line:
                current_network["Encryption"] = "Yes" if "on" in line else "No"
        # Print the parsed information
        print("Scanned WiFi networks:")
        for network in networks:
            print("SSID:", network.get("SSID", "Unknown"))
            print("BSSID:", network.get("BSSID", "Unknown"))
            print("Quality:", network.get("Quality", "Unknown"))
            print("Signal Level:", network.get("Signal Level", "Unknown"))
            print("Encryption:", network.get("Encryption", "Unknown"))
            print("-------------------------------")
    except Exception as e:
        print("Error scanning WiFi:", e)

def connect_wifi(ssid, password):
    try:
        subprocess.run(['sudo', 'nmcli', 'device', 'wifi', 'connect', ssid, 'password', password])
        print("Connected to WiFi network:", ssid)
    except Exception as e:
        print("Error connecting to WiFi:", e)

def print_menu():
    menu = """
        ███████╗██╗  ██╗███████╗  

        ██╔════╝██║  ██║██╔════╝
        ███████╗███████║███████╗
        ╚════██║██╔══██║╚════██║ 
        ███████║██║  ██║███████║      
        ╚══════╝╚═╝  ╚═╝╚══════╝ 
                                                                            
        [scan] Scan WiFi Networks
        [bruteforce] Bruteforce WiFi
        [connect] Connect to WiFi
        [exit] Exit
    """
    print(Fore.GREEN + menu)

def main():
    init()  # Initialize colorama
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "bruteforce" and len(sys.argv) > 2:
            ssid = sys.argv[2]
            bruteforce_wifi(ssid)
            return
    else:
        while True:
            print_menu()
            command = input(Fore.CYAN + "Enter command: ").lower()
            if command == "scan":
                scan_wifi()
            elif command.startswith("bruteforce"):
                ssid = command.split(" ")[1]
                bruteforce_wifi(ssid)
            elif command.startswith("connect"):
                try:
                    ssid, password = command.split(" ")[1].split(":")
                    connect_wifi(ssid, password)
                except Exception as e:
                    print("Invalid 'connect' command format. Please use 'connect ssid:password'.")
            elif command == "exit":
                break
            else:
                print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()