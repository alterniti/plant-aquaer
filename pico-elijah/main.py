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
import urequests

class Connect:
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

    def connect(self, ssid=None, testing_blink=False, testing_led=None):
        '''
        Automatically connects to nearby known networks \n
        If ssid arg given, connects to that network
        testing led feature doesn't work 
        '''
        if ssid:
            try:
                print(f"{ssid},{Connect.net_creds[ssid]["passw"]}")
                self.wlan.connect(ssid,Connect.net_creds[ssid]["passw"])
                while self.wlan.isconnected()==False:
                    print("waiting for connection...")
                    testing_led.blink(0.5) #type: ignore 
                print("connected")
                print(self.wlan.ifconfig())
            except:
                print(f"{ssid},{Connect.net_creds[ssid]["passw"]}")
                print("connection failed")
        else:
            print(f"\nAvailable networks:")
            nets_a=self.wlan.scan()
            nets_names=[]
            for net in nets_a:
                    print(f"{net[0]:20}{str(net[1])}")
                    nets_names.append(net[0].decode())
            print("\n=================================================")
            for saved_net in Connect.net_creds.values():
                if saved_net['ssid'] in nets_names:
                    print(f"connecting to {saved_net['ssid']}...")
                    try:
                        self.wlan.connect(saved_net['ssid'],saved_net['passw'])
                        if testing_blink==True:
                            testing_led.blink() # type: ignore
                        print("connected")
                        break
                    except:
                        print("connection failed")
                        if testing_blink==True:
                            testing_led.off() # type: ignore

    def ping(self,server_ip,password,data):
        pass

class Pump:
    all_units={}
    def __init__(self, pinid: int):
        self.control=machine.Pin(pinid, machine.Pin.OUT)
        self.pin=pinid
        self.name=f"PUMP.{self.pin}"
        self.info={self.name:{"control":self.pin,"class":self.__class__}}
        self.__class__.all_units.update(self.info)

    def on(self):
        self.control.on()

    def off(self):
        self.control.off()

class Led:
    all_units={}
    def __init__(
            self,
            pinid,
            color="WHITE"
        ):
        self.control=machine.Pin(pinid, machine.Pin.OUT)
        self.pin=pinid
        self.color=color
        self.name=f"LED{color}.{pinid}"
        self.info={self.name:{"color":self.color,"control":self.pin,"class":self.__class__}}
        self.__class__.all_units.update(self.info)

    def blink(self, duration=0.5):
        self.control.on()
        sleep(duration)
        self.control.off()
        sleep(duration)
    
    def on(self):
        self.control.on()

    def off(self):
        self.control.off()

class Sensor:
    all_units={}
    def __init__(self, s_type: str, pinIN: int,pinOUT: int):
        # params:
        # type:: MOISTURE or FLOW
        # pin:: GPID
        # moisture returns 44000 if 100 percent moisture
        self.name=f"{s_type}.{str(pinIN)}.{str(pinOUT)}"
        if s_type=="MOISTURE":
            self.s_type="MOISTURE"
            self.control=machine.Pin(pinOUT, machine.Pin.OUT)
            self.signal=machine.ADC(pinIN).read_u16()
        if s_type=="FLOW":
            self.s_type="FLOW"
            self.control=machine.Pin(pinOUT, machine.Pin.OUT)
            self.signal=machine.ADC(pinIN).read_u16()
        self.info={self.name:{"control":pinOUT,"signal":pinIN,"last_update":{"time":None,"data":None},"class":self.__class__}}
        self.__class__.all_units.update(self.info)

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
    
    def record_values(self):
        pass

class Main:
    global all_devices
    all_devices={}

    def __init__(self):
        '''
        Startup script
        '''
        print("==================================================\
            \nPlant Aquaer\nA project for PLTW's EDD course\n\nBy Gatlin Meyer, Brandon Peterson, and Elijah Ross\
            \n==================================================\n")
        
    def test_headless(self, led):
        while True:
            led.blink()
    
    def update_devices(self):
        all_devices.update(Sensor.all_units)
        all_devices.update(Pump.all_units)
        all_devices.update(Led.all_units)
        return all_devices

m=Main()
# the following are for testing purposes only. Feel free to   
# edit them as needed
led=Led("LED")
s1=Sensor("MOISTURE",28,20)
s2=Sensor("MOISTURE",27,21)
s3=Sensor("FLOW",26,19)
led2=Led(18)
pm=Pump(17)
for device in m.update_devices():
    print(device)
for x in range(1,3):    
    led.blink()
cnct=Connect()
cnct.connect(testing_led=led)
while not cnct.wlan.isconnected():
    led.off()
    print("connecting...")
    sleep(0.5)
print("connected")
led.on()

# m.test_headless(led)
# aioble.central.scan(10000, interval_us=12000, window_us=10000, active=True) #bluetooth testing