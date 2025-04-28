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
    """network connection object
    """
    
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

    def connect(self, ssid=None, testing_led=None):
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
                        if testing_led:
                            testing_led.blink() # type: ignore
                            while not cnct.wlan.isconnected():
                                testing_led.blink() #type: ignore
                                print("connecting...")
                            testing_led.on()
                        print("connected")
                        break
                    except:
                        print("connection failed")
                        if testing_led:
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
            color="WHITE",
        ):
        self.control=machine.Pin(pinid, machine.Pin.OUT)
        self.pin=pinid
        self.color=color
        self.name=f"LED{color}.{pinid}"
        self.info={self.name:{"color":self.color,"control":self.pin,"class":self.__class__}}
        self.__class__.all_units.update(self.info)

    def config_rgb(self, r_pin, g_pin, b_pin):
        self.r_pin=r_pin
        self.g_pin=g_pin
        self.b_pin=b_pin
        self.rgb_control=[machine.Pin(r_pin, machine.Pin.OUT),machine.Pin(b_pin, machine.Pin.OUT),machine.Pin(g_pin, machine.Pin.OUT)]
        self.color="RGB"
        self.name=f"LED{self.color}.{r_pin}-{g_pin}-{b_pin}"
        self.info={self.name:{"color":self.color,"control":self.rgb_control,"class":self.__class__}}
        self.__class__.all_units.update(self.info)

    def rgb_color(self, color):
        '''
        "w","r","g","b" for white, red, green, or blue respectively. 
        '''
        if color=="w":
            for i in self.rgb_control:
                i.on()
        if color=="r":
            self.rgb_control[0].on()
            self.rgb_control[1].off()
            self.rgb_control[2].off()
        if color=="g":
            self.rgb_control[0].off()
            self.rgb_control[1].on()
            self.rgb_control[2].off()
        if color=="b":
            self.rgb_control[0].off()
            self.rgb_control[1].off()
            self.rgb_control[2].on()

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
    """represents a sensor object\n
    
    Keyword arguments:\n
    s_type -- MOISTURE or FLOW\n
    pinIN -- the ADC pin from which data is read\n
    pinOUT -- the control pin; turns the sensor on or off\n
    Return: None
    """
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
            self.signal=machine.ADC(pinIN)
        if s_type=="FLOW":
            self.s_type="FLOW"
            self.control=machine.Pin(pinOUT, machine.Pin.OUT)
            self.signal=machine.ADC(pinIN).read_u16()
        self.info={self.name:{"control":pinOUT,"signal":pinIN,"last_update":{"time":None,"data":None},"class":self.__class__}}
        self.__class__.all_units.update(self.info)

    def get_moisture(self):
        self.control.on()
        sig=self.signal.read_u16()
        self.control.off()
        return int(sig)

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
    """main functions\n
    
    Keyword arguments:
    none
    Return: None
    """
    
    global all_devices
    all_devices={}

    def __init__(self):
        '''
        Startup script
        '''
        print("==================================================\
            \nPlant Aquaer\nA project for PLTW's EDD course\n\nBy Gatlin Meyer, Brandon Peterson, and Elijah Ross\
            \n==================================================\n")
        board_led=machine.Pin("LED",machine.Pin.OUT)
        for i in range(0,6):
            board_led.toggle()
            sleep(0.1)
        board_led.off()

    def config_devices(self):
        """Initializes the default device names and declares them as global

        Return: None
        """
        global pump0,moist0,moist1,moist2,led0,conn0
        #pump
        pump0=Pump(28)
        #sensors
        moist0=Sensor("MOISTURE",26,20)
        moist1=Sensor("MOISTURE",27,21)
        moist2=Sensor("MOISTURE",28,22)
        #indicator
        led0=Led("LED","GREEN")
        #connection
        conn0=Connect()

    def headless(self):
        global_cycles=-1
        self.config_devices()
        moist_threshold=36000
        led0.blink()
        while True:
            global_cycles+=1
            motor_cycles=0
            moisture=moist0.get_moisture()
            # moisture=(moist0.get_moisture()+moist1.get_moisture()+moist2.get_moisture())
            # moisture=moisture/3
            if moisture>moist_threshold:
                soil_moist=True
                prewater_moist=moisture
                while moisture>moist_threshold:
                    motor_cycles+=0
                    pump0.control.on()
                    print(f"pump ON | motor cycles: {motor_cycles} | moisture {moisture}")
                    sleep(5)
                    moisture=moist0.get_moisture()
                    # moisture=(moist0.get_moisture()+moist1.get_moisture()+moist2.get_moisture())
                    # moisture=moisture/3
                    if motor_cycles>1: #if been running for more than 20 secs
                        if prewater_moist-moisture<5000: # if the moisture hasn't really changed
                            print("make sure pump and hose are connected properly!")
                            pump0.control.off()
                            break
                pump0.off()
            else:
                soil_moist=False
                print(f"pump OFF | moisture: {moisture}")
            sleep(1)
            # sleep(60*60*24) #60 sec x 60 min x 24 hours
        
    def test_headless(self, led):
        while True:
            led.blink()

    def test_motor(self, motor, indicator=None, cycle_limit=None, interval=0.5):
        def toggle_motor():
            if indicator:
                indicator.control.toggle()
            motor.control.toggle()
            sleep(interval)
        if cycle_limit:
            for x in range(0,cycle_limit):
                toggle_motor()
        else:
            while True:
                toggle_motor()
    
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
pm=Pump(28)
for device in m.update_devices():
    print(device)

cnct=Connect()
cnct.connect(testing_led=led)

m.headless()

# m.test_motor(pm)