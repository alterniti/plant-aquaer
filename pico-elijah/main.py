# this will be the main file. 

# ↓↓↓ added 'type: ignore' to prevent 'module not found' errors ↓↓↓
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
            "pass":"pico-2-w@s"
        },
        "brandon-school-pc":{
            "ssid":"",
            "pass":""
        },
        "joseph-iphone":{
            "ssid":"Joseph's iPhone",
            "pass":"Please!!"
        },
        "elijah-laptop":{
            "ssid":"",
            "pass":""
        }
    }

    def __init__():
        pass

    def connect():
        pass

    def ping(server_ip,password,data):
        pass

class pump:
    def __init__():
        pass

    def pump_water(duration):
        pass

class sensors:
    def __init__(self, type: str, pin: int):
        # params:
        # type:: MOISTURE or FLOW
        # pin:: GPID
        name=type.join()
        return 

    def get_moisture():
        pass
    def is_moist():
        pass

    def get_flow(self):
        pass

class main:
    def init():
        print("Plant Aquaer\nA project for PLTW's EDD course\n\nBy Gatlin Meyer, Brandon Peterson, and Elijah Ross")

main.init()