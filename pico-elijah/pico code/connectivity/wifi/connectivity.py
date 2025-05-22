#example from https://core-electronics.com.au/guides/raspberry-pi-pico-w-connect-to-the-internet/

# A simple example that:
# - Connects to a WiFi Network defined by "ssid" and "password"
# - Performs a GET request (loads a webpage)
# - Queries the current time from a server

import network   # handles connecting to WiFi
import urequests # handles making and servicing network requests
import time
import socket
import machine
import rp2
import sys

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Fill in your network name (ssid) and password here:
ssid = "Joseph's iPhone" #'MININT-G8108QN 2215'
password = 'Please!!' #'67r5D0+4'
wlan.connect(ssid, password)

while wlan.isconnected()==False:
    print("connecting...")
    print(wlan.isconnected())
    time.sleep(0.5)
    print(wlan.status())


# Example 1. Make a GET request for google.com and print HTML
# Print the html content from google.com
print("1. Querying google.com:")
r = urequests.get("http://www.google.com")
print(r.content)
r.close()

# Example 2. urequests can also handle basic json support! Let's get the current time from a server
# print("\n\n2. Querying the current GMT+0 time:")
# r = urequests.get("http://date.jsontest.com") # Server that returns the current GMT+0 time.
# print(r.json())