import base64
import hmac
import urllib
import paho.mqtt.client as mqtt
import time

idScope = "0ne000BE51F"
deviceKey = "SharedAccessSignature sr=0ne000BE51F%2Fregistrations%2F002409020C00089D&skn=registration&sig=4zXeolxGxLKVWNqPkz0KB4M4KXDw0w8EdmQvQdCNBTM%3D&se=1995531517"
deviceId = "002409020C00089D"
dpsAddress = "global.azure-devices-provisioning.net"
dpsUser = idScope+ '/registrations/' + deviceId + '/api-version=2019-03-31'
endpoint = dpsAddress + '/devices/' + deviceId
dpsTopicPublish = '$dps/registrations/PUT/iotdps-register/?$rid=' + deviceId
dpsTopicSubscribe = '$dps/registrations/res/#'
dpsRegistrationMessage = '{\"registrationId\": \"' + deviceId + '\"}'

def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("Connection established with result code "+str(rc));
    else:
        print("Bad connection returned code: " + str(rc))
    client.subscribe(dpsTopicSubscribe)
    client.publish(dpsTopicPublish, dpsRegistrationMessage)
def on_publish(client, userdata, mid):
    print("Sent message")
def on_message(client, userdata, msg):
    print("{0} - {1} ".format(msg.topic, str(msg.payload)))
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected connection returned code: " + str(rc));
def on_Log(client, userdata, level, buf):
    print("Log: "+ buf)
def on_Disconnect(client, userdata, flags, rc=0):
    print("Disconnected connection returned code: " + str(rc));
def on_Message(client, userdata, msg):
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"));
    print("Message recieved by broker after publishing is " + str(m_decode));

client = mqtt.Client(client_id=deviceId, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect= on_disconnect
client.on_publish = on_publish
client.username_pw_set(username=dpsUser,password=deviceKey)
client.tls_set_context(context=None)
client.tls_insecure_set(True)
client.connect(dpsAddress, port=8883)
client.loop_forever()
