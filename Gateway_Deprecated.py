import random
import time
import sys
import json
import threading
import ast
from threading import Thread
import asyncio
import config as constants
import configparser
import RPi.GPIO as GPIO
from ConfigEditor import ConfigEditor
from send_heart_beat_worker import send_heart_beat_worker
from DeviceKeyVault import DeviceKeyVault
from DeviceConnection import DeviceConnection
from DeviceProvisioning import DeviceProvisioning
from DeviceMessaging import DeviceMessaging
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

device_client = None
config = ConfigEditor()
        
def Discovery_Switch(device_messaging):
    time.sleep(2)
    device_messaging.send_LPCU_discovery_signal()

def respond_to_message(message,device_messaging):
    print("Received message <------: " + str(message))
    device_messaging.acknowledge(message)
    device_messaging.respond(message)
    
def message_method_listener(device_client,device_messaging):
    while True:
        print("executed message method")
        method_request = device_client.receive_method_request("messagemethod")  # Wait for method2 calls
        payload = {"result": True, "data": 1234}  # set response payload
        status = 200  # set return status code
        device_messaging.send_method_response(method_request, status, payload)
        Data = method_request.payload
        respond_to_message(Data,device_messaging)
        
def generic_method_listener(device_client,device_messaging):
    while True:
        method_request = device_client.receive_method_request()  # Wait for unknown method calls
        payload = {"result": False, "data": "unknown method"}  # set response payload
        status = 400  # set return status code
        print("Executed generic method: " + method_request.name)
        device_messaging.send_method_response(method_request, status, payload)
        Data = method_request.payload
        respond_to_message(Data)

def twin_update_listener(device_client,device_messaging):
    while True:
        patch = device_client.receive_twin_desired_properties_patch()  # blocking call
        print("Twin patch received:")
        print(patch)
        patch_json = ast.literal_eval(str(patch))
        print(patch_json)
        for j in patch_json:
            print(patch_json[j])        
        #print("The data in the desired properties patch was: {}".format(patch))
        #respond_to_message(patch,device_messaging)
        
# define behavior for receiving a message
def message_listener(message,device_client,device_messaging):
    while True:
        #message = device_client.on_message_received()  # blocking call
        Data = message.data
        print("Offline Message received: " + str(Data))
        respond_to_message(json.loads(Data),device_messaging)

def message_received_handler(message):
    print("the data in the message received was ")
    print(message.data)
    print("custom properties are")
    print(message.custom_properties)
    print("content Type: {0}".format(message.content_type))
    print("")
        
# Define behavior for handling methods
async def method_request_handler(method_request):
    # Determine how to respond to the method request based on the method name
    if method_request.name == "method1":
        payload = {"result": True, "data": "some data"}  # set response payload
        status = 200  # set return status code
        print("executed method1")
    elif method_request.name == "method2":
        payload = {"result": True, "data": 1234}  # set response payload
        status = 200  # set return status code
        print("executed method2")
    else:
        payload = {"result": False, "data": "unknown method"}  # set response payload
        status = 400  # set return status code
        print("executed unknown method: " + method_request.name)

    # Send the response
    method_response = MethodResponse.create_from_method_request(method_request, status, payload)
    await device_client.send_method_response(method_response)
    
async def main():
    # Connect to key vault to get secrets
    key_vault = DeviceKeyVault(constants.DEVICE_UID)
    device_secret_recieved = key_vault.get_device_secret()
    print(device_secret_recieved) 
    if device_secret_recieved:
        # Connect to iot hub
        device_connection = DeviceConnection(constants.DEVICE_UID)
        device_client = device_connection.connect()
        # if failed then try registering the device
        if device_client == None:
            dps = DeviceProvisioning(constants.DEVICE_UID)
            registration_result = dps.register_device()
            if registration_result.status == 'assigned':
                device_client = device_connection.connect()
                if device_client == None:
                    raise RuntimeError("Unable to make a mqtt connection to the Iot hub")
            else:
                raise RuntimeError("Unable to register device to the Iot hub via DPS")
        print('Device connected successfully')
        if device_client is not None and device_client.connected:
            device_messaging = DeviceMessaging(device_client)
            #device_client.on_message_received = message_received_handler
            # Set the method request handler on the client
            device_client.on_method_request_received = method_request_handler
            
  
#            # Send firmware info and schedule heart beat messaging
#            send_heart_beat_thread = send_heart_beat_worker(device_messaging)
#            send_heart_beat_thread.daemon = True
#            send_heart_beat_thread.start()
#            # Call back for when the lpcu discoery switich is clicked
#            GPIO.add_event_detect(constants.SWITCH_IN_GPIO_PIN_ADDRESS, GPIO.RISING, callback=lambda x: Discovery_Switch(device_messaging), bouncetime=500)
#            # Run method listener threads in the background - Generic Direct Method
#            message_method_thread = threading.Thread(target=message_method_listener, args=(device_client,device_messaging))
#            message_method_thread.daemon = True
#            message_method_thread.start()
#            # Run method listener threads in the background - Message Direct Method
#            generic_method_thread = threading.Thread(target=generic_method_listener, args=(device_client,device_messaging))
#            generic_method_thread.daemon = True
#            generic_method_thread.start()
#            # Device twin thread
#            twin_update_listener_thread = threading.Thread(target=twin_update_listener, args=(device_client,device_messaging))
#            twin_update_listener_thread.daemon = True
#            twin_update_listener_thread.start()
#            # Run a listener thread in the background
#            listen_thread = threading.Thread(target=message_listener, args=(device_client,device_messaging))
#            listen_thread.daemon = True
#            listen_thread.start()
#            
            
            
        # Wait for user to indicate they are done listening for messages
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                send_heart_beat_thread.do_run = False
                send_heart_beat_thread.join()
                print("Quitting...")
                break
        
        device_connection.disconnect(device_client)
        device_client = None
        print('Device disconnected successfully')
    else:
        print('Device could not get secret from the vault!')
        
#####################################################
# EXECUTE MAIN
if __name__ == "__main__":
    asyncio.run(main())
    
    