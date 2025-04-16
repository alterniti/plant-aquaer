# this will be the main file. 

# ↓↓↓ added 'type: ignore' to prevent 'module not found' errors ↓↓↓
import machine #type: ignore
from machine import Pin #type: ignore
import network #type: ignore
import socket #type: ignore
import rp2 #type: ignore
import sys #type: ignore
from time import sleep #type: ignore

class connect:
    net_creds={
        "elija-school-pc":{
            "ssid":"Eli-comp",
            "passw":"pico-2-w@s"
        },
        "brandon-school-pc":{
            "ssid":"None",
            "passw":"None"
        },
        "joseph-iphone":{
            "ssid":"Joseph's iPhone",
            "passw":"Please!!"
        },
        "elijah-laptop":{
            "ssid":"None",
            "passw":"None"
        }
    }

    def __init__(self):
        # initializes network adapter
        self.wlan=network.WLAN(network.STA_IF)

    def list_networks(self):
        print(self.wlan.scan())

    def connect(self, ssid):
        print(f"Available networks:")
        nets_a=self.wlan.scan()
        for net in nets_a:
            print(net)
        for saved_net in connect.net_creds.items():
            if saved_net['ssid'] in nets_a:
                print("connecting to {saved_net['ssid']}...")
                try:
                    self.wlan.connect(saved_net['ssid'],saved_net['passw'])
                    print("connected")
                except:
                    print("connection failed")

                
        

    def ping(self,server_ip,password,data):
        pass

class pump:
    def __init__(self, pin: int):
        return f"pump{pin}"

    def pump_water(self, duration):
        pass

class sensors:
    def __init__(self, type: str, pin: int):
        # params:
        # type:: MOISTURE or FLOW
        # pin:: GPID
        name=type.join(str(pin))
        return name

    def get_moisture(self):
        pass
    def is_moist(self):
        pass

    def get_flow(self):
        pass


def startup():
    print("Plant Aquaer\nA project for PLTW's EDD course\n\nBy Gatlin Meyer, Brandon Peterson, and Elijah Ross")

connect().list_networks()
