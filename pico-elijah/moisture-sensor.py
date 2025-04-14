import machine
import time

moisture_sensor = machine.ADC(26)  # Moisture sensor connected to ADC pin 26
led = machine.Pin(27, machine.Pin.OUT)  # LED connected to GPIO pin 27
motor = machine.Pin(28, machine.Pin.OUT)  # Motor connected to GPIO pin 28

while True:
    # Read moisture level
    moisture_level = moisture_sensor.read_u16()
    print("Moisture Level:", moisture_level)
    
    # Check moisture level and control LED
    if moisture_level < 35000: 
        led.off()
        print("LED OFF: Soil is Moist")
        motor.off()  # Ensure motor is off when soil is moist
    else:
        led.on()
        print("LED ON: Soil is Dry")
        
        # Activate motor to pump water
        print("Motor ON: Pumping Water")
        motor.on()
        time.sleep(5)  # Run motor for 5 seconds
        motor.off()
        print("Motor OFF: Pump Stopped")
    
    time.sleep(2)
