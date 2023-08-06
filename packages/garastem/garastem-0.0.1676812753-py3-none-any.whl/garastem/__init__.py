import asyncio
import time
import threading
import garastem.version as version

from bleak import BleakClient, BleakScanner
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from termcolor import colored

UART_SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
UART_RX_CHAR_UUID = "0000ffe1-0000-1000-8000-00805f9b34fb"


try:
    import requests
    req = requests.get('https://pypi.org/pypi/garastem/json')
    package_info = req.json()
    latest_version = package_info['info']['version']
    if latest_version != version.version:
        print("Warning: Please update to latest version of this library")
except Exception as err:
    print(err)

print('Running version', version.version)

#! Coroutine setup, do not touch this magic block please
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
def create_task(coro):
    global loop
    loop.create_task(coro)
    if not hasattr(create_task, 'thread_started'):
        create_task.thread_started = True
        threading.Thread(target=loop.run_forever, daemon=True).start()
        

class GRobot:
    def __init__(self, name):
        self.name = name
        self.device = None
        self.client = None
        self.send_queues = []
        self.is_connected = False
        self.recvbuff = ''
        create_task(self.routine())
        
    
    async def routine(self):
        # start connect first
        while True:
            await asyncio.sleep(0.01)
            if not self.is_connected:
                device = await BleakScanner.find_device_by_filter(self._handle_filter)
                if device is None:
                    print(f'gr/ still finding {self.name}')
                    continue
                self.device = device
                self.client = BleakClient(
                    self.device,
                    disconnected_callback=self._handle_disconnect
                )
                await self.client.connect()
                
                self.is_connected = True
                print(f'gr/ {self.name} connected')
                await self.client.start_notify(UART_RX_CHAR_UUID, self._handle_rx)
            else:
                # Process the out data
                if len(self.send_queues):
                    send = self.send_queues.pop(0)
                    print('gs/ written\t', colored(send.strip(), 'yellow'))
                    send = bytes(send, 'utf8')
                    await self.client.write_gatt_char(UART_RX_CHAR_UUID, send)
                
                
    def write(self, data):
        self.send_queues.append(data)
            
    def _handle_rx(self, _: BleakGATTCharacteristic, data: bytearray):
        # print('gr/ data:', data)
        # pipe data
        self.recvbuff += data.decode('utf8')
        self.recvbuff = self.recvbuff.replace('\r\n', '\n').replace('\n', '')
        # print("DATA", self.recvbuff)
        print("gs/ received\t", colored(self.recvbuff, 'magenta'))
        self.recvbuff = ''
    
    def _handle_disconnect(self, _: BleakClient):
        self.is_connected = False
        print("gr/ device disconnected, retrying...")
        
    def _handle_filter(self, device: BLEDevice, adv: AdvertisementData):
        if device.name == self.name:
            print('Device Found: ', self.name)
            return True
        if device.name is not None:
            print('Found: ', device.name)
        return False
    
    def set_buzzer(self, state):
        if state:
            self.write('*B1#\r\n')
        else:
            self.write('*B0#\r\n')
    
    def stop(self):
        self.write('*M0|#\r\n')
    
    def move_forward(self, speed: float):
        speed = int(speed)
        self.write(f"M1|{'1' if speed < 0 else ''}{abs(speed)}#\r\n")
    
    def move_backward(self, speed: float):
        speed = int(speed)
        self.write(f"M2|{'1' if speed < 0 else ''}{abs(speed)}#\r\n")
    
    def rotate_left(self, speed: float):
        speed = int(speed)
        self.write(f"M3|{'1' if speed < 0 else ''}{abs(speed)}#\r\n")
    
    def rotate_right(self, speed: float):
        speed = int(speed)
        self.write(f"M4|{'1' if speed < 0 else ''}{abs(speed)}#\r\n")

    def set_motor(self, motor: int, speed: float):
        speed = int(speed)
        self.write(f"M{'5' if motor == 0 else '6'}|{'1' if speed < 0 else ''}{abs(speed)}#\r\n")
        
        

__all__ = [
    'GRobot'
]