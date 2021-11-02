import config as constants
import uuid
import time
import datetime
import json
import asyncio
import RPi.GPIO as GPIO
from datamodels import LpcuFirmwareInfo,UL_CFG_Body,LPCUDiscoverySignal,FirmwareInfo,FirmwareUpgradeProgress,FirmwareDownloadMsg,AcknowledgeMsg,Header,UL_RSCFG_Body,SCG_BUSY_Body,SCG_RCFG_Body,Report,SCG_RNET_Body,S_ON_Body,S_OFF_Body,CL_FWV_Body,CL_RSCFG_Body,CL_RCFG_Body
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse
from ConfigEditor import ConfigEditor
from DeviceKeyVault import DeviceKeyVault

class DeviceMessaging:
    
    def __init__(self,device_client):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(int(constants.LIGHT_OUT_GPIO_PIN_ADDRESS), GPIO.OUT)
        GPIO.setup(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, GPIO.OUT)
        GPIO.setup(constants.SWITCH_IN_GPIO_PIN_ADDRESS, GPIO.IN)
        GPIO.output(constants.LIGHT_OUT_GPIO_PIN_ADDRESS, False)
        self.config = ConfigEditor()
        self.device_client = device_client
#        print(self.config)
        self.firmwareversion_to_upgrade_to = self.config.getfirmwareValue('Firmware', 'firmwareversion_to_upgrade_to')
#        self.firmwareversion_to_upgrade_to = 2.23
        
    async def send(self, message, messageType = "Message"):
        if message != '':
            msg = Message(message)
            msg.message_id = uuid.uuid4()
            msg.correlation_id = "correlation-smrtscape"
            msg.custom_properties["Product"] = "Smrtscape"
            msg.custom_properties["MessageType"] = messageType
            await self.device_client.send_message(msg)
            print("Message(report) sent --------> " + message)
            await self.led_blink(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
        else:
            print("No return message sent")
    
    async def acknowledge(self, payload):
        # payload = json.loads(message)# set response payload
#         print(payload)
        messageId = payload.get("Id")
        header = payload.get('Header')
        body = payload.get('Body')
        
        header_payload = json.loads(header)
        body_payload = json.loads(body)
        
        uid = header_payload.get('UID')
        cmd = header_payload.get('CMD')
        cmd_org = body_payload.get('CMD_ORG')
        uid_org = body_payload.get('UID_ORG')
            
        # Send a message to mark message as received by id with success/failure code
        if cmd == 'UL_SLST':
            print('Command :' + str(cmd))
            acknowledgementMsg_Payload = AcknowledgeMsg(messageId,constants.DEVICE_UID,True,0,cmd_org,0,0,'UID_ORG:' + uid_org,True)
        else:
            acknowledgementMsg_Payload = AcknowledgeMsg(messageId,constants.DEVICE_UID)
        acknowledgementMsg = Message(json.dumps(acknowledgementMsg_Payload.__dict__))
        acknowledgementMsg.message_id = messageId
        acknowledgementMsg.correlation_id = "correlation-smrtscape"
        acknowledgementMsg.custom_properties["Product"] = "Smrtscape"
        acknowledgementMsg.custom_properties["MessageType"] = "Acknowledgement"
        await self.device_client.send_message(acknowledgementMsg)
        print("Acknowledge Message(report) sent for message id --------> " + str(messageId) + "\n")
        await self.led_blink(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
        
    async def respond(self, payload):               
        header = payload.get('Header')
        header_payload = json.loads(header)
        uid = header_payload.get('UID')
        cmd = header_payload.get('CMD')
        body = payload.get('Body')
        body_payload = json.loads(body)        
        pin = body_payload.get('PIN')
        if pin == None:
            pin = constants.DEVICE_PIN    
        s_id = body_payload.get('S_ID')
        dur = body_payload.get('DUR')        
        msg_id = payload.get("Id")            
        cmd_org = body_payload.get('CMD_ORG')
        uid_org = body_payload.get('UID_ORG')
        apan = body_payload.get('APAN')
        shid = body_payload.get('SHID')
        YEAR = datetime.date.today().year
        MONTH = datetime.date.today().month
        DATE = datetime.date.today().day
        HOUR = datetime.datetime.now().hour
        MINUTE = datetime.datetime.now().minute
        SECONDS = datetime.datetime.now().second
        returnMessage = ''
        headerOptions={
            'SCG_GCFG' : Header(uid,'SCG_RCFG',constants.DEVICE_UID),
            'SCG_GNET' : Header(uid,'SCG_RNET',constants.DEVICE_UID),
            'S_ON' : Header(uid,'S_ON',constants.DEVICE_UID),
            'S_ONT' : Header(uid,'S_ONT',constants.DEVICE_UID),
            'S_OFF' : Header(uid,'S_OFF',constants.DEVICE_UID),
            'UL_ADD' : Header(uid,'UL_CFG',constants.DEVICE_UID),
            'CL_GEVENT' : Header(uid,'CL_REVENT',constants.DEVICE_UID),
            'CL_ADD' : Header(uid,'CL_FWV',constants.DEVICE_UID),
            'CL_SCFG' : Header(uid,'CL_RSCFG',constants.DEVICE_UID),
            'CL_GCFG' : Header(uid,'CL_RCFG',constants.DEVICE_UID),
            'UL_SCFG' : Header(uid,'UL_RSCFG',constants.DEVICE_UID),
#             'SCG_SDSCVRMODE' : Header(uid,'UL_DSC',constants.DEVICE_UID),
#             'FW_UPGD' : Header(uid,'FW_UPGD',constants.DEVICE_UID),
#             'FW_DWNL' : Header(uid,'FW_DWNL',constants.DEVICE_UID),
        }
        
        header = headerOptions.get(cmd, "Unknown")
        bodyOptions={
            'SCG_GCFG' : SCG_RCFG_Body(uid,"SCG_RCFG",10,5,10,8192,0,222,6,7),
            'SCG_GNET' : SCG_RNET_Body('SCG_RNET',uid,1,'192.168.1.9','255.255.255.0','192.168.1.1','0.0.0.0','192.168.1.1','00:24:09:02:2b:50'),
            'S_ON' : S_ON_Body(int(pin),s_id,dur,'S_ON',uid,'None'),
            'S_ONT' : S_ON_Body(int(pin),s_id,dur,'S_ONT',uid,'None'),
            'S_OFF' : S_OFF_Body(int(pin),s_id,dur,'S_OFF',uid,'None'),
            'UL_ADD' : UL_CFG_Body('UL_CFG',apan,shid,YEAR,MONTH,DATE,HOUR,MINUTE,SECONDS,5,-8,1,33,-117,0,0,18,42,6,37,1,'dusk','22:00','disable','disable',127,'disable','disable','disable','disable',0,uid,pin,77,11,1,31,1,0,0,'4B21C0178888C78E00090209240035820615D5210923123500054D0B011F000001040021008B0115D500010001047FFF021600FD00FD00FD00FD00FD00FD0000'),
#             'UL_ADD' : 'QtgY5hW7sqZ1dFBhKoLc4t8hOthoAAAhnA78dlVX2hNwlffj26tvLW9mBMg4kRc17JyGGr7JBSrLZXMW/8IgSPbJ8Tx5WKMFBzN/59/BCKFmFiSbph6gD/5W6TuvXnxaUaVrBGuwcBTFpCo12ftCt4HFJNYOo6h4W88mAhUfjczWF3J/L9CpsudllJgcfjhYE05wQtQDf91vd5m2sLuTZxnTqBMkcUQgNWd3jc6///dh38hIdnKrPy7NskDh4imHu37perznpO4eARL6uoWQqzQ9Oxn+tJFnEDCXakzRvldBBkRd55sPYgCxU1SgF4fWxbmWkpQp5khVLKX482mmHxu8I7DgyjYt4nJohH8YN/UVl2hpYUQoEtWejvHhME2YzFfwTnk4wum8eYuxaSDuEC28ZY30dH8sppSejvHhME2YzLAxF8PaTNsYEAJMLxnzcEOUYfPgMW1qaPIoS8hN2vWpGn9+he2Fv3+UmDEEo3q5EDCsp6YQLZhtugQJAXq6O71XXQaMcxNIj5eyllfwZ5r+La7/yuOlwoMQArwaDOzArxyTmrR0ojQUaheM2VRgoleu2wzxvN/NeTlZJQDDx8vIpmJTf6fpUmSrEcrucbPe+46tyvSZaR5mshE5cgpLfWlnLnw9zS9VqcghpOqbMmjWNbbb6bKd7JcFzkGMHAKbEAKSlZ/L/xYKaQ9b3M0kgfEamk8Vg+7cYciI55QWmZ8AfnopAALKj0f8EDAaxBxvKVbCsKyQ6fdFjsC2AN5XrAIXtFix0DdiUQcfXJ0knlN5SOXwn7DgnXIHqB7/SXa3zIaDgT0ghT+rI1JBicfZUY+h54uZXUNRj6Hni5ldQ1GPoeeLmV1DJ7Mvhc4lwyo=',
            'CL_GEVENT' : 'wZQkp7CL24Y9mRkIEAJf7EF3b4i/hyF8yqd0Mz2dnQxZ0RyyabZRxp819Zyy0mxs8k8t4hAtPJX8q7LpBZz5lt+TSjHr6IqtVRqGEDC/OhAwZoKcFxu/PlKDCtTo9mC+VO8vWKb1lnM6DjJPHK8jXz5vB3DbF9VIPwTXS75cXxRnU7icvlxfFGdTuJyaWNNb1n46gYlxpjiRdPi40fenjNL3c4VkQmvFMerS6HcpOZC8fUrw/n3jEDCDNT0qvlxfFGdTuJxLLx8QMDZC0FeVelxpemhtaw==',            
            'CL_ADD' : CL_FWV_Body('CL_FWV',34,1,195,'KD2',109,13,13,109,'FFFFFFFF',apan,64642,uid,cmd_org),
            'CL_SCFG' : CL_RSCFG_Body('CL_RSCFG',uid,cmd_org,shid,apan,msg_id,'SUCCESS',0,'NULL'),
            'CL_GCFG' : CL_RCFG_Body('CL_RCFG','ADD_CTL',msg_id,uid,64642,2121,0,13,257,1,34,104,1,1,'000D1504020239012255AAAAAA2EF7E9A1200020164E1B3525C999E10749D4BB15071710130001000900000001FFFFFFFF','003A0803000000010100000100090100000009FF000000000000000000000015071710130005071715101301644C05574F3700000000000000000000','4B06000AFFFFFFFF','003C3C004B005A000102000000000000007F64000000780087009600000003040000000000FF64020000B400C300D200000000000506000000FF64000202','0060000000001410C000FC000C0000000000000027000300010000150515000D3400011500010009FF03000739323530340000640E820A00008B108E00F99700FA060B09DD00A6FE3B0055FD0221DB0E4504AE0755006B09BD0A2303298000800080','602400800000000000000000000000000000000024090202021CF50000000849FC8200010009'),
            'UL_SCFG' : UL_RSCFG_Body('UL_RSCFG',uid,'SUCCESS',0,'SUCCESS',0),
#             'SCG_SDSCVRMODE' : 'pysGCShCc7cJpHvKhgYF+smA8t1479OFzmzFZOr2R5j+++neQtdBTTNtIX/vv8BB1NrIoCBza9k6YxXlYgSe7u8doWJoPwnkrnvnlZaC63EKgtxqdRNgQ5qOc2esNRZO+uQe/nu2XNtgWD5ZX10ULvy1SlCB/KiZSaJxqmD7HcQ='
#             'FW_UPGD' : '',
#             'FW_DWNL' : '',
        }
        body = bodyOptions.get(cmd, "Unknown")
        rpt = Report(header,body)
        
        if cmd == 'S_ON':
            await self.led_on(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
        elif cmd == 'S_ONT':
            await self.led_on(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
        elif cmd == 'S_OFF':
            await self.led_off(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
                
        if body == 'Unknown':
            if cmd == 'FW_UPGD':
                FirmwareFiles = body_payload.get("FirmwareFiles")
                print(FirmwareFiles)
                for file in FirmwareFiles:                    
                    print(file["FID"])
                totalBYT = 885264
                firmwareVersionToBe = self.config.getfirmwareValue('Firmware', 'firmwareversion_to_upgrade_to')
                firmwareversion = self.config.getfirmwareValue('Firmware', 'firmwareversion')
#                print(str(firmwareVersionToBe))
                await self.sendFirmwareUpdateProgress(uid,firmwareversion,0,0,apan,shid,cmd_org,uid_org)
                await self.setSCGBusyStatus(constants.DEVICE_UID,10000,cmd)
                await self.getFirmwareFileSegment(uid,596,constants.segmentLength,0)
                self.config.setfirmwareValue('Firmware', 'continue_firmware_upgrade_process','True')
#             elif cmd == 'FW_DWNL':
                print(self.config.getfirmwareValue('Firmware', 'continue_firmware_upgrade_process'))
                if self.config.getfirmwareValue('Firmware', 'continue_firmware_upgrade_process') == 'True':
                    cmd = header_payload.get('CMD')
                    stbyt = header_payload.get("stbyt")
                    stbyt = 0
                    # Body is encrypted .. no decryption available on the pi ... hence the hard coded value
                    #totalBYT = 885264
                    totalBYT = 24576
                    while int(((stbyt+constants.segmentLength)/totalBYT)*100) < 100 and self.config.getfirmwareValue('Firmware', 'continue_firmware_upgrade_process') == 'True':
                        print(str(int(((stbyt+constants.segmentLength)/totalBYT)*100)))
                        await self.sendFirmwareUpdateProgress(uid,firmwareversion,int(((stbyt+constants.segmentLength)/totalBYT)*100),1,apan,shid,cmd_org,uid_org)
                        await self.setSCGBusyStatus(constants.DEVICE_UID,5000,cmd)
                        await self.getFirmwareFileSegment(uid,596,constants.segmentLength,stbyt+constants.segmentLength)
                        stbyt = stbyt+constants.segmentLength
                        time.sleep(10)
                    perc = 100
                     # Set the new firmware version number in the config
                    old_firmwareversion = self.config.getfirmwareValue('Firmware', 'firmwareversion')
                    old_lpcu_firmwareversion = self.config.getfirmwareValue('Firmware', 'lpcu_firmwareVersion')
                    old_kd2_firmwareversion = self.config.getfirmwareValue('Firmware', 'kd2_firmwareversion')
                    self.config.setfirmwareValue('Firmware', 'continue_firmware_upgrade_process','False')
                    firmwareVersion = self.config.setfirmwareValue('Firmware', 'firmwareversion',self.config.getfirmwareValue('Firmware', 'firmwareversion_to_upgrade_to'))
#                    lpcu_firmwareVersion = self.config.setfirmwareValue('Firmware', 'lpcu_firmwareVersion',self.config.getfirmwareValue('Firmware', 'lpcu_firmwareVersion_to_upgrade_to'))
#                    kd2_firmwareVersion = self.config.setfirmwareValue('Firmware', 'kd2_firmwareversion',self.config.getfirmwareValue('Firmware', 'kd2_firmwareVersion_to_upgrade_to'))
                    await self.send_gateway_firmware_info()
#                    await self.send_lpcu_firmware_info(s_id,apan,shid,pin,uid)
#                    await self.send_kd2_firmware_info(msg_id,s_id,apan,shid,pin,uid)
                    await self.acknowledge(payload)
                    device_message = DeviceKeyVault(constants.DEVICE_UID)
                    device_message_recieved = device_message.get_device_message()                    
                    if not device_message_recieved == None:
#                         time.sleep(3)
                        await self.acknowledge(device_message_recieved)  
#                     time.sleep(3)
                    await self.sendFirmwareUpdateProgress(uid,firmwareversion,perc,2,apan,shid,cmd_org,uid_org)
#                     time.sleep(3)
#                     await self.setSCGBusyStatus(constants.DEVICE_UID,0,cmd)
                    
#                     time.sleep(15)
#                     firmwareVersion = self.config.setfirmwareValue('Firmware', 'firmwareversion',old_firmwareversion)
#                     lpcu_firmwareVersion = self.config.setfirmwareValue('Firmware', 'lpcu_firmwareVersion',old_lpcu_firmwareversion)
#                     kd2_firmwareVersion = self.config.setfirmwareValue('Firmware', 'kd2_firmwareversion',old_kd2_firmwareversion)                                     
                else:
                    print("xxxxx ---> Firmware upgrade process cancelled")
                    self.config.setfirmwareValue('Firmware', 'continue_firmware_upgrade_process','False') 
                    time.sleep(35)
                    self.config.setfirmwareValue('Firmware', 'continue_firmware_upgrade_process','True')      
            elif cmd == 'FW_CANCEL':
                print("yyyyyy ---> Firmware upgrade process cancel request received")
                self.config.setfirmwareValue('Firmware', 'continue_firmware_upgrade_process','False')
                print(self.config.getfirmwareValue('Firmware', 'continue_firmware_upgrade_process'))
            elif cmd == 'SCG_SDSCVRMODE':
                time.sleep(5)
                await self.send_LPCU_discovery_signal(uid,s_id,apan,shid,pin)
            else:
                print("Unknown command received, no response was sent --------> " + cmd)
        else:
            print("Is continuing firmware upgrade process? --------> " + self.config.getfirmwareValue('Firmware', 'continue_firmware_upgrade_process') )                        
            await self.send(rpt.toJSON())
            if cmd == 'S_ONT':
                print("timer sleep for " + str(60 * dur) + " seconds ") 
#                await asyncio.sleep(60 * dur)
                await asyncio.sleep(3)
                await self.led_off(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
            elif cmd == 'UL_SCFG':
                time.sleep(5)
                await self.setSCGBusyStatus(constants.DEVICE_UID,0,cmd)
                time.sleep(5)
                await self.send_gateway_firmware_info()
            elif cmd == 'UL_ADD':
                await self.send_lpcu_firmware_info(s_id,apan,shid,pin,uid)
        await self.led_blink(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
   
    async def getFirmwareFileSegment(self,device_id,fileid,seglen,stbyt):
        FirmwareDownloadMsg_Payload = FirmwareDownloadMsg(fileid,seglen,stbyt,device_id);
        FirmwareDownloadMsg_Body = json.dumps(FirmwareDownloadMsg_Payload.__dict__)
        await self.send(FirmwareDownloadMsg_Body,"FirmwareDownload")
        
    async def setSCGBusyStatus(self,device_id,milliseconds,cmd):
#         temp = '{"Header": {"UID":"' + device_id + '","CMD":"SCG_BUSY"},"Body": "{\\"UID\\": \\"' + device_id + '\\",\\"DUR\\": ' + str(milliseconds) + ',\\"OP\\": \\"FW_UPGD\\",\\"CMD\\": \\"SCG_BUSY\\"}"}'
        header = Header(device_id,'SCG_BUSY',constants.DEVICE_UID)
        body = SCG_BUSY_Body(device_id,str(milliseconds),cmd,'SCG_BUSY')
        rpt = Report(header,body)
        await self.send(rpt.toJSON())
            
    async def sendFirmwareUpdateProgress(self,device_id,firmwareversion,percent,status,apan,shid,cmd_org,uid_org):
        header = Header(device_id,'FW_PRGS',constants.DEVICE_UID)
        body = FirmwareUpgradeProgress("FW_PRGS",percent,device_id,firmwareversion,6,7,apan,shid,status,cmd_org,uid_org);
        rpt = Report(header,body)
        await self.send(rpt.toJSON())
#         firwareUpgradeProgress_Payload = FirmwareUpgradeProgress("FW_PRGS",percent,device_id,13,6,7,0,0,0,None,None);
#         firwareUpgradeProgress_body = json.dumps(firwareUpgradeProgress_Payload.__dict__)
#         firwareUpgradeProgress_body = firwareUpgradeProgress_body.replace('"','\\"')
#         tempreturnMessage = '{"Header": {"UID":"' + device_id + '","CMD":"FW_PRGS"},"Body": "' + firwareUpgradeProgress_body + '"}'            
#         await sendMessage(tempreturnMessage)

    async def send_method_response(self,method_request, status, payload):
        method_response = MethodResponse.create_from_method_request(method_request, status, payload)
        await self.device_client.send_method_response(method_response)  # send response
        
    async def send_heart_beat(self):
        #payload = json.dumps({'heartbeat': 'true'})
        payload = 'Heartbeat'
        await self.send(payload, payload)
            
    async def send_gateway_firmware_info(self):     
        firmwareVersion = self.config.getfirmwareValue('Firmware', 'firmwareversion')
#        firmwareVersion = firmwareVersion.replace('.', '')
#         firmwareMessage = '{"Header": {"UID":"' + constants.DEVICE_UID + '","CMD":"SCG_EVENT"},"Body": "VGNXvDAMISlj/bNBgwzlGnPkA4pAjk5FRbYhbKUnsdWckLx6jOnQTMkSCFJiKbcKEVonot6v5i9WkCiEtG0Y5r+JRq5biHaYuhxSl2njUx740ztXm5aa5jqdobDjz/WLdTpsu3UuLmFW+9QodTZMN/QrhZy3kJ+BxPuN8vGxG2t9q4ebUqEHdIRfM5B4lTZ6tInI96m8JEnQDkJLzy0M79PlAFnSB6kGKVOiFTpRJXxgCMxjjyC4xjZYhJHJ3wHBWHvhOqEWFtr7WVWjwhoqqiuF/HLW+OiffMGrDszrNjVOWqME3w5w/cV8OgaAbXTCjgO8BiDXvKU="}'
#         firmwareMessage = '{"Header": {"UID":"' + constants.DEVICE_UID + '","CMD":"SCG_EVENT"},"Body": "{\\"CMD\\": \\"SCG_EVENT\\",\\"F_VER\\": ' + firmwareVersion + ',\\"H_VER\\": 6,\\"B_VER\\": 7,\\    "UID\\": \\"002409020C000CD1\\",\\"TRIG\\": 1,\\"TEMP\\": 20,\\"SW1\\": 1,\\"DHCP\\": 1,\\    "IP_ADR\\": \\"192.168.1.26\\",\\"SBNET\\": \\"255.255.255.0\\",\\"DNS1\\": \\"192.168.1.1\\",\\"DNS2\\": \\"0.0.0.0\\",\\"GTWY\\": \\"192.168.1.1\\",\\"MAC\\": \\"00:24:09:02:0c:d1\\"}"}'
#         await self.send(firmwareMessage)
        header = Header(constants.DEVICE_UID,'SCG_EVENT',constants.DEVICE_UID)
        body = FirmwareInfo("SCG_EVENT",firmwareVersion,6,7,constants.DEVICE_UID,1,20,1,1,'192.168.1.26','255.255.255.0','192.168.1.1','0.0.0.0','192.168.1.1','00:24:09:02:0c:d1');
        rpt = Report(header,body)
        await self.send(rpt.toJSON())
        print(f'Firmware info sent to the server - ' + firmwareVersion)
        reported_props = {"F_VER": firmwareVersion,"H_VER": firmwareVersion,"B_VER": firmwareVersion}
        await self.device_client.patch_twin_reported_properties(reported_props)
        print( "Device twins updated with latest firmwareVersion")
    
    async def send_lpcu_firmware_info(self,s_id,apan,shid,pin,uid):     
        lpcu_firmwareVersion = self.config.getfirmwareValue('Firmware', 'lpcu_firmwareversion')
        lpcu_firmwareVersion = lpcu_firmwareVersion.replace('.', '')
        header = Header(uid,'UL_EVENT',constants.DEVICE_UID)
        # body = FirmwareInfo("UL_EVENT",1,5589,1,9999,50,11,1,0,uid);
        body = LpcuFirmwareInfo("UL_EVENT",1,apan,shid,pin,lpcu_firmwareVersion,11,1,0,uid)
        rpt = Report(header,body)
        await self.send(rpt.toJSON())
        print(f'LPCU Firmware info sent to the server - ' + lpcu_firmwareVersion)
        
    async def send_kd2_firmware_info(self,msg_id,s_id,apan,shid,pin,uid):     
        kd2_firmwareVersion = self.config.getfirmwareValue('Firmware', 'kd2_firmwareversion')
        kd2_firmwareVersion = kd2_firmwareVersion.replace('.', '')
        header = Header(uid,'CL_RCFG',constants.DEVICE_UID)       
#        body = CL_RCFG_Body('CL_RCFG','ADD_CTL',msg_id,uid,64642,2121,0,13,257,1,34,kd2_firmwareVersion,1,1,
        body = CL_RCFG_Body('CL_RCFG','ADD_CTL',msg_id,uid,shid,apan,0,13,257,1,34,kd2_firmwareVersion,1,1,'000D1504020239012255AAAAAA2EF7E9A1200020164E1B3525C999E10749D4BB15071710130001000900000001FFFFFFFF','003A0803000000010100000100090100000009FF000000000000000000000015071710130005071715101301644C05574F3700000000000000000000','4B06000AFFFFFFFF','003C3C004B005A000102000000000000007F64000000780087009600000003040000000000FF64020000B400C300D200000000000506000000FF64000202','0060000000001410C000FC000C0000000000000027000300010000150515000D3400011500010009FF03000739323530340000640E820A00008B108E00F99700FA060B09DD00A6FE3B0055FD0221DB0E4504AE0755006B09BD0A2303298000800080','602400800000000000000000000000000000000024090202021CF50000000849FC8200010009')
        rpt = Report(header,body)
        await self.send(rpt.toJSON())
        print(f'kd2 Firmware info sent to the server - ' + kd2_firmwareVersion)
        
    async def send_LPCU_discovery_signal(self,uid,s_id,apan,shid,pin):
        header = Header(constants.LPCU_DEVICE_UID,'UL_DSC',constants.DEVICE_UID)
#         body = LPCUDiscoverySignal("UL_DSC",1,34952,1,6207,77,11,1,1,uid)
#         body = LPCUDiscoverySignal("UL_DSC",s_id,apan,shid,pin,77,11,1,1,uid)
        body = LPCUDiscoverySignal("UL_DSC",1,34592,1,6207,77,11,1,1,uid)
        rpt = Report(header,body)
        print(f'LPCU discovery signal sent ')
        await self.send(rpt.toJSON())
        await self.led_blink(constants.LIGHT_OUT_GPIO_PIN_ADDRESS)
        
    async def led_blink(self,pin_address):                
        GPIO.output(pin_address, not GPIO.input(pin_address))
        time.sleep(constants.BLINK_TIMESPAN / 1000.0)
        GPIO.output(pin_address, not GPIO.input(pin_address))
#         GPIO.output(pin_address, GPIO.HIGH)
#         time.sleep(constants.BLINK_TIMESPAN / 1000.0)
#         GPIO.output(pin_address, GPIO.LOW)
        
    async def led_on(self,pin_address):
        GPIO.output(pin_address, GPIO.HIGH)
        
    async def led_off(self,pin_address):
        GPIO.output(pin_address, GPIO.LOW)




