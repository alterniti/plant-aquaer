import network
import time

# WiFi credentials
ssid = "Eli-comp"
password = "pico-2-w@s"

# Initialize the WiFi interface
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connect to the WiFi network
wlan.connect(ssid, password)

# Wait for the connection to establish
while not wlan.isconnected():
    print("Connecting to network...")
    time.sleep(1)
     