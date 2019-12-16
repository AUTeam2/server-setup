from django.shortcuts import render
from django.http import HttpResponse
from demo_module.messagehandler.client import MqttClient
from demo_module.messagehandler import protocol
from django.template import loader


# Create your views here.

def send_mqtt(request):

    # Create a message to send
    topic = "demo_module/inbound"

    # Payload
    m = protocol.Message()
    m.new()
    m.sentBy = "Team 2"
    m.msgType = "data"
    m.statusCode = "200"
    m.dataObj = {
        'x': [1,2,3,4,5,6,7,8,9,10],
        'y': [1,4,9,16,25,36,49,64,81,100]
    }

    # Get ready to send
    m.pack()
    send_me = protocol.ProtocolSchema.write_jsonstr(m.payload)

    # The donothing function
    def donothing(client, userdata, message):
        pass

    # Create client
    publisher = MqttClient("MessageSender", donothing)

    # Send and disconnect
    rc = publisher.publish(topic, send_me)
    publisher.disconnect()

    # Render a response
    template = loader.get_template('message_sent.html')

    if rc:
        outcome = "Success. Message was sent."
    else:
        outcome = "Failure. Message was not sent."

    context = {'outcome': outcome,
               'topic': topic,
               'msg': send_me}

    return HttpResponse(template.render(context, request))