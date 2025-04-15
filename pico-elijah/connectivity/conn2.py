import network
import socket
from time import sleep
import machine
import rp2
import sys
from machine import Pin

ssid = 'Eli-comp'
password = 'pico-2-w@s'

led = Pin('LED', Pin.OUT) #create a pin object

def blink():
    led.value(not led.value())

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        wlan.scan()
        print('Waiting for connection...')
        print(wlan.status())
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')


connect()
while True:
    blink()
    sleep(0.5)