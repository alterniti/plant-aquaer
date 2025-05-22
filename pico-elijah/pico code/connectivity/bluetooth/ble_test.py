# from kevsrobots on youtube

import aioble
import bluetooth
import asyncio
import struct
from sys import exit 
import machine
from machine import Pin
import time

# define UUIDs for service / characteristic
_SERVICE_UUID = bluetooth.UUID(0x1848)
_CHARACTERISTIC_UUID = bluetooth.UUID(0x2A6E)

IAM = "central"

if IAM not in ['peripheral', 'central']:
    print("IAM must be either peripheral or central")
    exit()

if IAM=="central":
    IAM_SENDING_TO = "peripheral"
else: 
    IAM_SENDING_TO = "central" 

MESSAGE = f"Hello from {IAM}!"

#bluetooth params

BLE_NAME = f"{IAM}" 
BLE_SVC_UUID = bluetooth.UUID(0x181A)
BLE_CHARACTERISTIC_UUID = bluetooth.UUID(0x2A6E)
BLE_APPEARANCE = 0X0300
BLE_ADVERTISING_INTERVAL = 2000
BLE_SCAN_LENGTH = 5000
BLE_WINDOW = 30000

# state variables
message_count = 0

# board led
led = machine.Pin("LED", machine.Pin.OUT)

def encode_message(message):
    return message.encode('utf-8')

def decode_message(message):
    return message.decode('utf-8')

async def send_data_task(connection, characteristic):
    ''' Send data to the connected device'''
    global message_count
    while True:
        if not connection:
            print("error - no connection in send data")
            continue

        if not characteristic:
            print('error - no characteristic provided in send data')
            continue

        message = f"{MESSAGE} {message_count}"
        message_count += 1
        print(f"sending {message}")

        try:
            msg = encode_message(message)
            characteristic.write(msg)

            await asyncio.sleep(0.5)
            response = decode_message(characteristic.read())

            print(f"{IAM} sent: {message}, response {response}")
        except Exception as e:
            print(f"writing error {e}")

        await asyncio.sleep(0.5)

async def receive_data_task(characteristic):
    """receive data from the connected device"""
    global message_count
    while True:
        try:
            data = await characteristic.read()

            if data:
                print(f"{IAM} received: {decode_message(data)}, {dir(characteristic.connection.services())} count: {message_count}")
                # await asyncio.sleep(0.5)
                await characteristic.write(encode_message("Got it!"))
                await characteristic.write(encode_message(""))
                await asyncio.sleep(0.5)

            message_count += 1 

        except asyncio.TimeoutError:
            print(f"Timeout waiting for data in {BLE_NAME}.")
            break
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

        """
        ['__class__', '__init__', '__module__', '__qualname__', '__str__', 'read', 
        'write', '__dict__', '_check', '_connection', '_end_handle', '_find', 
        '_notified_indicated', '_notify_event', '_notify_queue', '_on_indicate', 
        '_on_notify', '_on_notify_indicate', '_read_data', '_read_done', 
        '_read_event', '_read_result', '_read_status', '_register_with_connection', 
        '_start_discovery', '_value_handle', '_write_done', '_write_event', 
        '_write_status', 'connection', 'descriptor', 'descriptors', 'indicated', 
        'notified', 'properties', 'service', 'subscribe', 'uuid']

        connection attributes: 
            ['__class__', '__init__', '__module__', '__qualname__', '__aenter__', 
            '__aexit__', '__dict__', 'disconnect', 'mtu', 'timeout', 
            '_characteristics', '_conn_handle', '_connected', '_discover', 
            '_event', '_l2cap_channel', '_mtu_event', '_pair_event', '_run_task', 
            '_task', '_timeouts', 'authenticated', 'bonded', 'device', 'device_task', 
            'disconnected', 'encrypted', 'exchange_mtu', 'is_connected', 'key_size', 
            'l2cap_accept', 'l2cap_connect', 'pair', 'service', 'services']

                services() attributes/functions
                ['__class__', '__init__', '__module__', '__qualname__', '__aiter__', 
                '__anext__', '__dict__', '_args', '_connection', '_disc_type', 
                '_discover_done', '_discover_result', '_event', '_parent', '_queue', 
                '_start', '_status', '_timeout_ms']
        """

async def run_peripheral_mode():
    # set up ble service and characteristic
    ble_service = aioble.Service(BLE_SVC_UUID)
    characteristic=aioble.Characteristic(
        ble_service,
        BLE_CHARACTERISTIC_UUID,
        read=True, 
        notify=True,
        write=True,
        capture=True
    )
    aioble.register_services(ble_service)

    print(f"{BLE_NAME} starting to advertise")

    while True:
        async with await aioble.advertise(
            BLE_ADVERTISING_INTERVAL,
            name=BLE_NAME,
            services=[BLE_SVC_UUID],
            appearance=BLE_APPEARANCE
        ) as connection:
            print(f"{BLE_NAME} connected to another device: {connection.device}")

            tasks = [
                asyncio.create_task(send_data_task(connection,characteristic))
            ]
            await asyncio.gather(*tasks)
            print(f"{IAM} disconnected")
            break

async def ble_scan():
    print(f"Scanning for BLE Beacon named {BLE_NAME}...")

    async with aioble.scan(BLE_SCAN_LENGTH, interval_us=BLE_ADVERTISING_INTERVAL, window_us=BLE_WINDOW, active=True) as scanner:
        async for result in scanner:
            result.charList = ""
            result.nameAttr = str(result.name())
            result.manuList = []
            for item in result.services():
                result.charList=f"\"{str(item)}\""
            print(f"    name: {str(result.name()):<25} services: {result.charList:<20}  rssi: {result.rssi}\n      {result}")
            if result.name() == IAM_SENDING_TO and BLE_SVC_UUID in result.services():
                print(f"found {result.name()} with service uuid {BLE_SVC_UUID}")
                return result
    return None

"""
reuslt attributes
['__class__', '__init__', '__module__', '__qualname__', '__str__', '__dict__',
'adv_data', 'connectable', 'name', 'resp_data', 'rssi', '_decode_field', '_update', 
'device', 'manufacturer', 'services', 'charList', 'nameAttr', 'manuList']
"""

async def run_central_mode():
    #start scanning for a device with the matching service UUID
    while True:
        device = await ble_scan()

        if device is None:
            continue
        print(f"device is: {device}, name is {device.name()}")

        try:
            print(f"Connecting to {device.name()}")
            connection = await device.device.connect()

        except asyncio.TimeoutError:
            print("Timeout during connection")
            continue

        print(f"{IAM} connected to {connection}")

        #discover services
        async with connection:
            try:
                service = await connection.service(BLE_SVC_UUID)
                characteristic = await service.characteristic(BLE_CHARACTERISTIC_UUID)
            except (asyncio.TimeoutError, AttributeError):
                print("Timed out discovering services/characteristics")
                continue
            except Exception as e:
                print(f"Error discovering services {e}")
                await connection.disconnect()
                continue

            tasks = [
                asyncio.create_task(receive_data_task(characteristic))
            ]
            await asyncio.gather(*tasks)

            await connection.disconnected()
            print(f"{BLE_NAME} disconnected from {device.name()}")
            break

async def main():
    while True:
        if IAM == "central":
            tasks = [
                asyncio.create_task(run_central_mode())
            ]
        else:
            tasks = [
                asyncio.create_task(run_peripheral_mode())
            ]
        
        await asyncio.gather(*tasks)

led.off()
for i in range(0,6):
   led.toggle()
   time.sleep(0.1)
asyncio.run(main())