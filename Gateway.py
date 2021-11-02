# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information. Majunu
# --------------------------------------------------------------------------

import os
import asyncio
import threading
from six.moves import input
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
#from azure.iot.device.common.transport_exceptions import UnauthorizedError

import json
import ast
import config as constants
import configparser
import RPi.GPIO as GPIO
import time

from ConfigEditor import ConfigEditor
from DeviceKeyVault import DeviceKeyVault
from DeviceConnection import DeviceConnection
from DeviceProvisioning import DeviceProvisioning
from DeviceMessaging import DeviceMessaging

async def main():
    device_client = None
    config = ConfigEditor()
    
     # Connect to key vault to get secrets
    key_vault = DeviceKeyVault(constants.DEVICE_UID)
    is_device_secret_recieved = key_vault.get_device_secret()
    if is_device_secret_recieved:
        try:          
            print('DEVICE_UID: ' + constants.DEVICE_UID)
            device_client = IoTHubDeviceClient.create_from_symmetric_key(
                        symmetric_key=config.getValue('Device', 'DeviceSymmetricKey'),
                        hostname=config.getValue('Device', 'AssignedIotHub'),
                        device_id=constants.DEVICE_UID,
                    )
            await device_client.connect()
        except Exception as ex:
            dps = DeviceProvisioning(constants.DEVICE_UID)
            registration_result = dps.register_device()
            if registration_result.status == 'assigned':
                device_client = IoTHubDeviceClient.create_from_symmetric_key(
                        symmetric_key=config.getValue('Device', 'DeviceSymmetricKey'),
                        hostname=config.getValue('Device', 'AssignedIotHub'),
                        device_id=constants.DEVICE_UID,
                    )
                await device_client.connect()
            else:
                raise RuntimeError("Unable to register device to the Iot hub via DPS")    
         
        if device_client == None:
            raise RuntimeError("Unable to make a mqtt connection to the Iot hub")        
    else:
        raise RuntimeError("Unable to get device secret from the key vault")
    
    async def respond_to_message(message):
        print("Received message <------: " + str(message))                        
        if not ('RESCMD' in str(message) or 'FW_UPGD' in str(message)):
            await device_messaging.acknowledge(message)
        await device_messaging.respond(message)
        
    # Define behavior for handling methods
    async def method_request_handler(method_request):
        # Determine how to respond to the method request based on the method name
        if method_request.name == "messagemethod":
            payload = {"result": True, "data": "some data"}  # set response payload
            status = 200  # set return status code
            Data = method_request.payload            
        else:
            payload = {"result": False, "data": "unknown method"}  # set response payload
            status = 400  # set return status code
            print("executed generic method: " + method_request.name)
            Data = method_request.payload        
        # Send the response
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        await device_client.send_method_response(method_response)
        await respond_to_message(Data)
        
    # define behavior for receiving a message
    # NOTE: this could be a function or a coroutine
    async def message_received_handler(message):
        Data = message.data
        print("Offline Message received: " + str(Data))
        await respond_to_message(json.loads(Data))
       
    async def twin_patch_handler(patch):
        print("the data in the desired properties patch was: {}".format(patch))        
        print(patch)
        patch_json = ast.literal_eval(str(patch))
        print(patch_json)
        for j in patch_json:
            print(patch_json[j])        
        #print("The data in the desired properties patch was: {}".format(patch))
        #respond_to_message(patch,device_messaging)
    
    # define send message to iot hub
    async def send_heart_beat(device_client,device_messaging):
        #payload = json.dumps({'heartbeat': 'true'})
        await device_messaging.send_gateway_firmware_info()
        payload = 'Heartbeat'
        while True:
            await device_messaging.send(payload)
#            await device_client.send_message(telemetry_data)
            await asyncio.sleep(constants.HEARTBEAT_DELAY)
                
    def send_heart_beat_sync(device_client,device_messaging):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(send_heart_beat(device_client,device_messaging))
    
    def push_discovery_switch(device_client,device_messaging):
        time.sleep(2)
        device_messaging.send_LPCU_discovery_signal()
        
    # Define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break
    
    if device_client is not None and device_client.connected:
        device_messaging = DeviceMessaging(device_client)            
        # Set the handlers on the client
        device_client.on_message_received = message_received_handler
        device_client.on_method_request_received = method_request_handler
        device_client.on_twin_desired_properties_patch_received = twin_patch_handler
        
    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
    
    # Call back for when the lpcu discoery switich is clicked
    GPIO.add_event_detect(constants.SWITCH_IN_GPIO_PIN_ADDRESS, GPIO.RISING, callback=lambda x: push_discovery_switch(device_client,device_messaging), bouncetime=500)

    send_heart_beat_Thread = threading.Thread(target=send_heart_beat_sync, args=(device_client,device_messaging))
    send_heart_beat_Thread.daemon = True
    send_heart_beat_Thread.start()
    
#    push_discovery_switch_Thread = threading.Thread(target=push_discovery_switch, args=(device_client,device_messaging))
#    push_discovery_switch_Thread.daemon = True
#    push_discovery_switch_Thread.start()
    
    # Wait for user to indicate they are done listening for method calls
    await user_finished    
    await device_client.disconnect()
    # Finally, shut down the client
    #await device_client.shutdown()


if __name__ == "__main__":
#    GPIO.setmode(GPIO.BCM)
#    GPIO.setup(int(constants.LIGHT_OUT_GPIO_PIN_ADDRESS), GPIO.OUT)
#    GPIO.setup(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, GPIO.OUT)
#    GPIO.setup(constants.SWITCH_IN_GPIO_PIN_ADDRESS, GPIO.IN)
#    GPIO.output(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, False)
#    GPIO.output(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, GPIO.HIGH)
#    time.sleep(120)
#    GPIO.output(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, GPIO.LOW)
    asyncio.run(main())

    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()


