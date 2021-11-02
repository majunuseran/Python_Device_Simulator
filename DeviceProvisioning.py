import config as constants
import base64
import hmac
import hashlib

from azure.iot.device import ProvisioningDeviceClient
from ConfigEditor import ConfigEditor

class DeviceProvisioning:

    def __init__(self,deviceUID):
        self.deviceUID = deviceUID
        self.config = ConfigEditor()
        
    def register_device(self):
        symmetric_key = self.derive_device_key()
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=constants.PROVISIONING_HOST,
            registration_id=constants.DEVICE_UID,
            id_scope=constants.ID_SCOPE,
            symmetric_key=symmetric_key,
        )
#         provisioning_device_client.provisioning_payload = {"modelId": model_id}
        registration_result = provisioning_device_client.register()
        if registration_result.status == 'assigned':
            self.config.setValue('Device', 'DeviceSymmetricKey', symmetric_key)
            self.config.setValue('Device', 'AssignedIotHub', registration_result.registration_state.assigned_hub)
            self.config.setValue('Device', 'ConnectionString', '')
            print("Device provisioned successfully <------>: " + str(registration_result.registration_state.assigned_hub))
        return registration_result
    
    def derive_device_key(self):
        deviceuid = constants.DEVICE_UID.encode("utf-8")
        signing_key = base64.b64decode(constants.ENROLLMENT_GROUP_SYMMETRIC_KEY.encode("utf-8"))
        signed_hmac = hmac.HMAC(signing_key, deviceuid, hashlib.sha256)
        device_key_encoded = base64.b64encode(signed_hmac.digest())
        return device_key_encoded.decode("utf-8")
    