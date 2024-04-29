#import apsystems_api as EZ1
from APsystemsEZ1 import APsystemsEZ1M as EZ1
from configparser import ConfigParser
from paho.mqtt import client as mqtt_client
import asyncio
import time
import sys

FIRST_RECONNECT_DELAY = 1
RECONNECT_RATE = 2
MAX_RECONNECT_COUNT = 12
MAX_RECONNECT_DELAY = 60

def connect_mqtt(client_id, broker, port):
    def on_connect(self, client, userdata, flags, rc):
    # For paho-mqtt 2.0.0, you need to add the properties parameter.
    # def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Set Connecting Client ID
    # client = mqtt_client.Client(client_id)

    # For paho-mqtt 2.0.0, you need to set callback_api_version.
    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)

    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, int(port))
    return client

def publish(client, topic, msg):
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")



def main():
    config = ConfigParser()
    config.read('config.ini')

    # maybe create a config class to handle all config and defaults
    # Default config
    home = config['Base']['home']
    single_run = config.getboolean('Base', 'single_run')

    # Inverter config
    inverter_ip = config['APsystems']['inverter_ip']
    inverter_port = config['APsystems']['inverter_port']

    # mqtt config
    mqtt_broker = config['mqtt']['broker']
    mqtt_port = config['mqtt']['port']
    mqtt_prefix = config['mqtt']['prefix']
    client_id = config['mqtt']['client_id']


    # Initialize the inverter with the specified IP address and port number.
    inverter = EZ1(inverter_ip, inverter_port)

    #Device info
    # return (
    #     ReturnDeviceInfo(
    #         deviceId=response["data"]["deviceId"],
    #         devVer=response["data"]["devVer"],
    #         ssid=response["data"]["ssid"],
    #         ipAddr=response["data"]["ipAddr"],
    #         minPower=int(response["data"]["minPower"]),
    #         maxPower=int(response["data"]["maxPower"]),
    #     )
    #     if response and response.get("data")
    #     else None
    info = inverter.get_device_info()
    if info != None:
        print ("get Device info")
        status = inverter.get_device_power_status()
        if status > 0:
            print("power is off")
        else:
            print("power ist on")
            output = inverter.get_output_data()

    else:
        print ("Not Device info cancle this round")

    # Iniialize MQTT object
    # mqtt = connect_mqtt(client_id, mqtt_broker, mqtt_port)                         
    # mqtt.loop_start()  

    # while (single_run):
    #     # check status of microinverter
    #     # ist status is offline no values need to be published
    #     



    #     # collect microinverter live data



    #     print("publish Test message...")
    #     # ret = mqtt.publish(mqtt_prefix + "inverter/test","1")
    #     time.sleep(5)
    


if __name__ == '__main__':
    main()