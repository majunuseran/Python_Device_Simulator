import base64
import hmac
import hashlib

from base64 import b64encode, b64decode, encode 
from hashlib import sha256 
from time import time 
from urllib import quote_plus, urlencode 
from hmac import HMAC 

def generate_sas_token(uri, key, policy_name, expiry=360000000): 
    ttl = time() + expiry 
    sign_key = "%s\n%d" % ((quote_plus(uri)), int(ttl)) 
    signature = b64encode(HMAC(b64decode(key), sign_key.encode('utf-8'), sha256).digest()) 
    rawtoken = { 
        'sr' :  uri, 
        'sig': signature, 
        'se' : str(int(ttl)), 
        'skn' : policy_name 
    }
    return 'SharedAccessSignature ' + urlencode(rawtoken) 

def derive_device_key(deviceId, EnrollmentGroupKey):
        deviceId = deviceId.encode("utf-8")
        signing_key = base64.b64decode(EnrollmentGroupKey.encode("utf-8"))
        signed_hmac = hmac.HMAC(signing_key, deviceId, hashlib.sha256)
        device_key_encoded = base64.b64encode(signed_hmac.digest())
        return device_key_encoded.decode("utf-8")
        
myIdScope = '0ne000BE51F'
deviceId = '002409020C00089D'
EnrollmentGroupKey = 'zpMTkIXzSCF0EUZnmKD0E58Q0AzfDGpsaCotMwmD0Vxeb+V83iIeQ4KE71wo61SoWUDUD7xFRdOxdR2be7eBfQ=='
DeviceKey = derive_device_key(deviceId, EnrollmentGroupKey)
print(DeviceKey)
print(generate_sas_token(myIdScope+"/registrations/"+deviceId, DeviceKey, "registration"))
