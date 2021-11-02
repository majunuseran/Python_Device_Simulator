import json 
import requests
import config as constants
from ConfigEditor import ConfigEditor

class DeviceKeyVault:

    def __init__(self,deviceUID):
        self.deviceUID = deviceUID
        self.config = ConfigEditor()
        self.AuthorizationHeaderValue = 'Basic ?uid=' + constants.DEVICE_UID + '&Password=TestGatewayType1'
        
    def get_device_secret(self):
        print('Getting Device secret .... ')
        getDeviceSecret_result = False
        URL = constants.KEYVAULT_URL

        headers = {'Accept': 'application/json',
                   'user-agent': 'customize header string',
                   'Content-Type': 'application/json; charset=utf-8',
                   'Authorization' : self.AuthorizationHeaderValue}  

        API_KEY = "Api_key"
        USER_KEY = "Key"
        USERNAME = "Name"

        params = {
          "apikey": API_KEY,
          "userkey": USER_KEY,
          "username": USERNAME
        }

        response = requests.get(URL,headers = headers,params=params)
        
        #print(response.headers)
        #print(response.headers['Content-Type'])
        
        if response.status_code != 200:
            print('Device secret request returned an error: ' + str(response.status_code))
        else:
            if str(response.text).find('0ne000BE51F') != -1:
                print("Device secret recieved successfully <------>: " + str(response.text))
                # set ENROLLMENT_GROUP_SYMMETRIC_KEY, ID_SCOPE
                getDeviceSecret_result = True
            else:
                print("Device secret recieved did not match expected <------>: " + str(print(response.text)))
                
        return getDeviceSecret_result
    
    def get_device_message(self):
        print('Getting Device latest message .... ')
        getDeviceMessage_result = False
        URL = constants.CHECK_MESSAGES_URL        
        headers = {'Accept': 'application/json',
                   'user-agent': 'customize header string',
                   'Content-Type': 'application/json; charset=utf-8',
                   'Authorization' : self.AuthorizationHeaderValue}  

        API_KEY = "Api_key"
        USER_KEY = "Key"
        USERNAME = "Name"

        params = {
          "apikey": API_KEY,
          "userkey": USER_KEY,
          "username": USERNAME
        }

        response = requests.get(URL,headers = headers,params=params)
        if response.status_code != 200:
            print('Device messages request returned an error: ' + str(response.status_code))
            getDeviceSecret_result = None
        else:
            print("Device message recieved successfully <------>: " + str(response.text))
            getDeviceSecret_result = json.loads(response.text.replace('[','').replace(']',''))
        return getDeviceSecret_result




