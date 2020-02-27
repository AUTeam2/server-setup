"""
Contains view functions for the demo_module
URL paths that lead here are in demo_module/urls.py
"""

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.template import loader

from demo_module.messagehandler.client import MqttClient
from demo_module.messagehandler import protocol
from .forms import TestForm
from .models import Result, Status

import json


# Show landing page for the demo module
def demo_main_page(request):
    return render(request, 'demo_module/home.html')


# Show test creation form for the demo module
def demo_create_test(request):

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


# show running test page will include webcam feed
def demo_running_test(request):
    #Not done
    return render(request, 'demo_module/running_test.html')


# show saved test page
def saved_data(request):
    # import all test, when database is implementet uncomment these
    # all_test = Date_list.objects.all()
    # context = {"all_test" : all_test}
    # return render(request, '/demo_module/templates/saved_data.html',context)
    return render(request, 'demo_module/saved_data.html')


# Show specific data page, specific datapoints from a test from saved_data
class show_data(ListView):
    #model = Result
    template_name = 'demo_module/show_data.html'


#All saved tests
class ResultListView(ListView):
    model = Result
    queryset = Result.objects.all().order_by('-job_received_time')


#Info page about the demo module
class StatusListView(ListView):
    model = Status
    queryset = Status.objects.all()


# busy page, test already running
def demo_busy(request):
    return render(request, 'demo_module/busy.html')

# def send_mqtt(request):
#
#     # Create a message to send
#     topic = "demo_module/inbound"
#
#     # Payload
#     m = protocol.Message()
#     m.new()
#     m.sentBy = "Team 2"
#     m.msgType = "data"
#     m.statusCode = "200"
#     m.dataObj = {
#         'x': [1,2,3,4,5,6,7,8,9,10],
#         'y': [1,4,9,16,25,36,49,64,81,100]
#     }
#
#     # Get ready to send
#     m.pack()
#     send_me = protocol.ProtocolSchema.write_jsonstr(m.payload)
#
#     # The donothing function
#     def donothing(client, userdata, message):
#         pass
#
#     # Create client
#     publisher = MqttClient("MessageSender", donothing)
#
#     # Send and disconnect
#     rc = publisher.publish(topic, send_me)
#     publisher.disconnect()
#
#     # Render a response
#     template = loader.get_template('demo_module/message_sent.html')
#
#     if rc:
#         outcome = "Success. Message was sent."
#     else:
#         outcome = "Failure. Message was not sent."
#
#     context = {'outcome': outcome,
#                'topic': topic,
#                'msg': send_me}
#
#     return HttpResponse(template.render(context, request))
