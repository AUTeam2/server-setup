import time

import source.protocol as pr
from source.client import MqttClient

PROTOCOL_SCHEMA_PATH = "protocol_v1_1.schema"
__VERSION__ = 1.1
ID = "demo_stub"
TOPOUT = "Testdevice/demo_module/Inbound"
TOPIN = "Testdevice/demo_module/Outbound"

status = 600

scheme = pr.ProtocolSchema.load_schema(PROTOCOL_SCHEMA_PATH)


def execution(orders):
    if orders.commandList[0] == "start":
        if orders.parameterObj.get("wait"):
            time.sleep(int(orders.parameterObj.get("wait")))

        data = {"x": ['Demo', 9, 10], "y": [16, 25, 36]}
        answer(orders.sentBy, "200", __VERSION__, "data", data)
        return
    else:
        answer(orders.sentBy, "405", __VERSION__, "status", {})


def answer(sender, state, version, typeof, data):
    """
    The function for answering a message
    :return:
    """
    global status
    status = state
    ans = pr.Message()
    ans.new()
    ans.protocolVersion = version
    ans.sentBy = sender
    ans.statusCode = state
    ans.msgType = typeof
    ans.dataObj = data
    # ans.dataObj = {"x": ['Demo', 9, 10], "y": [16, 25, 36]}

    ans.pack()

    if not pr.ProtocolSchema.validating(ans.payload, scheme):
        print('Pack your stuff in an orderly fashion!')
        print('Message wasnt sent!')
        return

    letter = pr.ProtocolSchema.write_jsonstr(ans.payload)
    ts.publish(TOPOUT, letter)
    print('Message sent.. :)')


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
    # schema_validation_result = pr.ProtocolSchema.validating(obj, m.protocol_schema)
    if not pr.ProtocolSchema.validating(obj, m.protocol_schema):
        print("Validation failed!")
        answer(ID, "400", __VERSION__, "status", {})
        return

    m.unpack(**obj)
    if m.msgType == "command":
        execution(m)

    if m.msgType == "status":
        answer(ID, status, __VERSION__, "status", {})


# Pass the callback to the client
ts = MqttClient(ID, on_message_callback)
time.sleep(5)
answer(ID, "600", __VERSION__, "status", {})

# Only subscribe to relevant inbound messages
ts.subscribe(TOPIN)

print("Starting listening loop")
ts.loop()
