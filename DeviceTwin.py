import json
import requests
from azure.iot.device import IoTHubModuleClient

import time
import threading
from threading import Thread
import config as constants
import configparser
import asyncio
from ConfigEditor import ConfigEditor

class DeviceTwin(Thread):
    def __init__(self,device_messaging):
        Thread.__init__(self)
        self.device_messaging = device_messaging
        self.config = ConfigEditor()
    
    def device_twin_update_listener(client):
        while True:
        patch = client.receive_twin_desired_properties_patch()  # blocking call
        print("Twin patch received:")
        print(patch)
        
    def run(self):
        print(f'Sending heart beat once every hour')
        currentThread = threading.currentThread()
        self.device_messaging.send_firmware_info()
        while getattr(currentThread, "do_run", True):
            self.device_messaging.send_heart_beat()
            #event.wait(constants.HEARTBEAT_DELAY)
            time.sleep(constants.HEARTBEAT_DELAY)
        print("Stopping Heartbeat messaging.")