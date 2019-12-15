import paho.mqtt.client as mqtt
from demo_module.messagehandler.protocol import Payload

#should we use pickle to save a dict?

class MqttClient():

    # These should be gotten from the environment or, ideally, from the Django settings file
    broker_address = "mqtt"   # this should be the name of the docker-compose service # "auteam2.mooo.com"
    broker_port = 1883
    username = "team2"
    password = "team2"
    will_message = "I'm Dying"

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

    @staticmethod
    def on_message(client, userdata, msg):
        p2 = Payload()
        print("1!")
        p2.message = msg.payload.decode("utf-8")
        p2.unpack()
        print(str(msg.topic) + ":")
        for key, value in p2.value.items():
            print(key + ": ", end='')
            print(value)

    @staticmethod
    def on_log(client, userdata, level, buf):
        print("log: ", buf)

    def __init__(self, name):
        """ Handles all setup and connection when object is initialized. """
        self.client = mqtt.Client(client_id=name, clean_session=True, userdata=None, transport="tcp")
        self.client.username_pw_set(MqttClient.username, MqttClient.password)
        self.client.on_connect = MqttClient.on_connect
        self.client.on_message = MqttClient.on_message
        self.client.on_log = MqttClient.on_log
        self.client.enable_logger()
        self.client.will_set(name, MqttClient.will_message)
        self.client.connect(MqttClient.broker_address)

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def loop(self):
        self.client.loop_forever(retry_first_connection=False)

    def async_loop(self):
        self.client.loop_start()

if __name__ == "__main__":

    team2_publisher = MqttClient("Team2TalksALot")

    team2_publisher.subscribe("#")

    p = Payload()
    p.sentBy = "Janus"
    p.msgType = "Command"
    p.pack()

    print("Publishing something")
    team2_publisher.publish("PythonMessage", str(p.message))

    print("Starting loop")
    team2_publisher.loop()

    print("Goodbye!")