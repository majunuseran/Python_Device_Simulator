import config as constants
from azure.iot.device import IoTHubDeviceClient
from ConfigEditor import ConfigEditor

class DeviceConnection:

    def __init__(self,deviceUID):
        self.deviceUID = deviceUID
        self.config = ConfigEditor()

    async def connect(self):
        try:
            device_client = IoTHubDeviceClient.create_from_symmetric_key(
                symmetric_key=self.config.getValue('Device', 'DeviceSymmetricKey'),
                hostname=self.config.getValue('Device', 'AssignedIotHub'),
                device_id=self.deviceUID,
            )
#            # Connect the client.
            await device_client.connect()
            return device_client
        except Exception as ex:
            return None
        
    async def disconnect(self,device_client):
        # Disconnect the client.
        await device_client.disconnect()
