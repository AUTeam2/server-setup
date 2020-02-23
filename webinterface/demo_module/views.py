"""
Contains view functions for the demo_module
URL paths that lead here are in demo_module/urls.py
"""

from django.shortcuts import render
from django.http import HttpResponse
from demo_module.messagehandler.client import MqttClient
from demo_module.messagehandler import protocol
from django.template import loader
from .forms import TestForm
import json

# Show landing page for the demo module
def demo_home(request):
    return render(request, 'demo_module/home.html')

# Show test creation form for the demo module
def demo_make_test(request):

    if request.method == 'POST':
        form = TestForm(request.POST)

        # Validate form
        if form.is_valid():
            # Do something with it, e.g. store it and send the MQTT message
            print("Form submitted!")

            template = loader.get_template('demo_module/message_sent.html')

            # Attempt to transmit MQTT-message based on validated form data
            if (transmit_mqtt(form.cleaned_data)):
                outcome = "Succes. Beskeden blev sendt."
            else:
                outcome = "Fejl. Beskeden blev ikke."

            # Show result to user
            context = {'outcome': outcome, }
            return HttpResponse(template.render(context, request))

    # GET-request, possibly failed submission
    else:
        # instantiate a new form to pass into the template context
        form = TestForm()

    # Render the form template
    return render(request, 'demo_module/make_test.html', {'form': form})


def transmit_mqtt(form_obj):
    """
    This function is not a view.
    This function transmits a validated message.
    """

    # Print to console for debug
    print(form_obj)

    # Create a message to send
    topic = form_obj['topic']
    # Payload
    m = protocol.Message()
    m.new()
    m.sentBy = form_obj['sender']
    m.msgType = form_obj['msg_type']
    m.statusCode = form_obj['status_code']

    # try-except on the json conversions
    # convert json -> python
    try:
        m.commandList = json.loads(form_obj['command_list_str'])
    except:
        print("Error converting commandlist -> insert empty")

    try:
        m.dataObj = json.loads(form_obj['data_obj_str'])
    except:
        print("Error converting dataObj -> insert empty")

    try:
        m.parameterObj = json.loads(form_obj['parameter_obj_str'])
    except:
        print("Error converting parameterObj -> insert empty")

    # Done inserting data
    m.pack()
    send_me = protocol.ProtocolSchema.write_jsonstr(m.payload)

    # debug output to console
    print(send_me)

    # Send it

    # The donothing callback function
    def donothing(client, userdata, message):
        pass

    # Create client
    publisher = MqttClient("DemoModuleMessageSender", donothing)

    # Send and disconnect
    rc = publisher.publish(topic, send_me)
    publisher.disconnect()

    return rc


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
    template = loader.get_template('demo_module/message_sent.html')

    if rc:
        outcome = "Success. Message was sent."
    else:
        outcome = "Failure. Message was not sent."

    context = {'outcome': outcome,
               'topic': topic,
               'msg': send_me}

    return HttpResponse(template.render(context, request))