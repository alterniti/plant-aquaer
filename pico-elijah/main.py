# this will be the main file. 

# ↓↓↓ added 'type: ignore' to prevent 'module not found' errors ↓↓↓
import machine #type: ignore
from machine import Pin #type: ignore
import network #type: ignore
import socket #type: ignore
import rp2 #type: ignore
import sys #type: ignore
from time import sleep #type: ignore
import aioble 

class connect:
    net_creds={
        "Eli-comp":{
            "ssid":"Eli-comp",
            "passw":"pico-2-w@s"
        },
        "brandon-pc":{
            "ssid":"brandon-pc",
            "passw":None
        },
        "Joseph's iPhone":{
            "ssid":"Joseph's iPhone",
            "passw":"Please!!"
        },
        "VICTUS-LAPTOP 0612":{
            "ssid":"VICTUS-LAPTOP 0612",
            "passw":"1M;2y905"
        }
    }

    def __init__(self):
        # initializes network adapter
        self.wlan=network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def list_networks(self):
        print(self.wlan.scan())

    def connect(self, ssid):
        '''
        Automatically connects to nearby known networks \n
        If ssid arg given, connects to that network
        '''
        if ssid:
            try:
                print(f"{ssid},{connect.net_creds[ssid]["passw"]}")
                self.wlan.connect(ssid,connect.net_creds[ssid]["passw"])
                while self.wlan.isconnected()==False:
                    print("waiting for connection...")
                    sleep(1)
                print("connected")
                print(self.wlan.ifconfig())
            except:
                print(f"{ssid},{connect.net_creds[ssid]["passw"]}")
                print("connection failed")
        else:
            print(f"Available networks:")
            nets_a=self.wlan.scan()
            nets_names=[]
            for net in nets_a:
                    print(f"{net[0]:20}{str(net[1])}")
                    nets_names.append(net[0].decode())
            print("\n==================================================")
            for saved_net in connect.net_creds.values():
                if saved_net['ssid'] in nets_names:
                    print(f"connecting to {saved_net['ssid']}...")
                    try:
                        self.wlan.connect(saved_net['ssid'],saved_net['passw'])
                        print("connected")
                        break
                    except:
                        print("connection failed")

    def ping(self,server_ip,password,data):
        pass

class pump:
    def __init__(self, pin: int):
        self.control=machine.Pin(pin, machine.Pin.OUT)
        return f"pump{pin}"

    def on(self):
        self.control.on()

    def off(self):
        self.control.off()        

class sensors:
    def __init__(self, s_type: str, pinIN: int,pinOUT: int):
        # params:
        # type:: MOISTURE or FLOW
        # pin:: GPID
        # moisture returns 44000 if 100 percent moisture
        name=s_type.join(str(pinIN).join(str(pinOUT)))
        if s_type=="MOISTURE":
            self.s_type="MOISTURE"
            self.control=machine.Pin(pinOUT, machine.Pin.OUT)
            self.signal=machine.ADC(pinIN).read_u16()
        if s_type=="FLOW":
            self.s_type="FLOW"
            self.control=machine.Pin(pinOUT, machine.Pin.OUT)
            self.signal=machine.ADC(pinIN).read_u16()
        return name

    def get_moisture(self):
        self.control.on()
        sig=self.signal
        self.control.off()
        return sig

    def is_moist(self,threshold=35000):
        '''
        params:
        threshold:: default is 35000. If the analog response is below this it returns True\n
        gets moisture from moisture sensor \n
        returns boolean
        '''
        if not self.s_type=="MOISTURE":
            print("invalid sensor")
            raise TypeError
        self.control.on()
        sig=self.signal
        self.control.off()
        if sig < threshold: 
            return True
        else:
            return False

    def get_flow(self):
        '''
        gets analog signal from flow meter
        '''
        return self.signal


def startup():
    '''
    Startup script
    '''
    print("==================================================\
          \nPlant Aquaer\nA project for PLTW's EDD course\n\nBy Gatlin Meyer, Brandon Peterson, and Elijah Ross\
          \n==================================================\n")

startup()
# aioble.central.scan(10000, interval_us=12000, window_us=10000, active=True) #bluetooth testing

# connect().connect(None) 