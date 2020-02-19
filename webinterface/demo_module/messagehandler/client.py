"""
This module implements a custome MQTT client, which can be of two types:
- Subscriber: Listens for messages on a given topic
- Publisher: Sends messages on a given topic

Uses Django's settings module, where the MQTT-settings are stored

"""

import paho.mqtt.client as mqtt
from django.conf import settings

class MqttClient():

    # These should be gotten from the environment or, ideally, from the Django settings file
    broker_address = settings.MQTT["internal"]["HOST"]
    broker_port = settings.MQTT["internal"]["PORT"]
    username = settings.MQTT["internal"]["USER"]
    password = settings.MQTT["internal"]["PASSWORD"]

    # This method is the same for all instances of the class
    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    # For outputting log messages to console
    @staticmethod
    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    # By default, do nothing on_message
    @staticmethod
    def on_message_default(client, userdata, message):
        pass

    #Initialize the client, straight on create
    def __init__(self, name, on_message, will_message="Logging off"):
        """ __init__ Handles all setup and connection when object is initialized.
        @:param: name is the name of the client, as will be shown on the server (required)
        @:param: on_message is the callback used when this client receives a message (required)
        @:param: will_message is the "Last Will" message sent when the client loses the connection (optional)
        """
        self.client = mqtt.Client(client_id=name, clean_session=True, userdata=None, transport="tcp")
        self.client.username_pw_set(MqttClient.username, MqttClient.password)
        self.client.on_connect = MqttClient.on_connect
        self.client.on_message = on_message

        # In production, let's consider disabling logging or routing to a file
        self.client.on_log = MqttClient.on_log
        self.client.enable_logger()

        # This ensures, that there is some sort of goodbye on losing connection
        self.client.will_set(name, will_message)

        # Connect immediately
        self.client.connect(MqttClient.broker_address)

    def publish(self, topic, payload):
        return self.client.publish(topic, payload)

    def subscribe(self, topic):
        return self.client.subscribe(topic)

    def loop(self):
        return self.client.loop_forever(retry_first_connection=False)

    def disconnect(self):
        return self.client.disconnect()

    # def async_loop(self):
    #     self.client.loop_start()