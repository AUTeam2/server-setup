import time

import source.protocol as pr
from source.client import MqttClient

PROTOCOL_SCHEMA_PATH = "protocol_v1_0.schema"
__VERSION__ = 1.0
ID = "demo_module"
TOPOUT = "demo_module/inbound"
TOPIN = "demo_module/outbound"

status = "600"

scheme = pr.ProtocolSchema.load_schema(PROTOCOL_SCHEMA_PATH)


def answer():
    global status
    """
    The function for answering a message
    :return:
    """
    ans = pr.Message()
    ans.new()
    ans.protocolVersion = __VERSION__
    ans.sentBy = ID
    ans.statusCode = status
    ans.msgType = "data"
    ans.dataObj = {"x": ['Demo', 9, 10], "y": [16, 25, 36]}

    ans.pack()
    letter = pr.ProtocolSchema.write_jsonstr(ans.payload)
    time.sleep(2)
    ts.publish(TOPOUT, letter)


def answer_command(com):
    global status
    if com == "start" and status != "610":
        status = "200"

    elif com == "start" and status == "610":
        status = "610"

    elif com == "stop":
        status = "200"
    else:
        status = "405"

    print("Command request")
    print(status)
    answer()

    if com == "start" and status == "200":
        status = "610"

    if com == "stop" and status == "200":
        status = "600"


def answer_data(state):
    global status
    if state == 1:
        status = "500"
        answer()
    else:
        status = "400"
        answer()


def on_message_callback(client, userdata, message):
    """
    The function executed when receiving a message

    :param client:
    :param userdata:
    :param message:
    :return:
    """
    # Creates an object for the incoming message
    m = pr.Message()

    msg = message.payload

    obj = pr.ProtocolSchema.read_jsonstr(msg)

    # Evaluate if the Python object conforms to the protocol
    schema_validation_result = pr.ProtocolSchema.validating(obj, m.protocol_schema)
    if schema_validation_result:
        print("Validation ok")
    else:
        print("Validation failed!")

    m.unpack(**obj)

    if not schema_validation_result:
        answer_data(2)

    elif m.msgType == "status":
        print("Status request")
        print(status)
        answer()


    elif m.msgType == "command":
        answer_command(m.commandList[0])

    elif m.msgType == "data":
        print("Data")
        print(status)
        answer_data(1)

    else:
        print("Wrong kinda message...")
        answer_data(2)


# Pass the callback to the client
ts = MqttClient("demostub", on_message_callback)
time.sleep(5)
answer()

# Only subscribe to relevant inbound messages
ts.subscribe(TOPIN)

print("Starting listening loop")
ts.loop()
