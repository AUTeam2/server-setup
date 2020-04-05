"""
Contains view functions for the demo_module
URL paths that lead here are in demo_module/urls.py
"""

from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.generic import ListView
from django.template import loader
from datetime import datetime
from django.conf import settings

from comms.messagehandler.client import MqttClient
from comms.messagehandler import protocol
from .forms import TestForm, AccelerometerForm
from .models import Result, Status, Inbound_teststand_package, ND_TS


# Bokeh for charts
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import HoverTool, ResetTool, FreehandDrawTool

# Numpy for data
import numpy as np
from numpy import fft as fft

import json

def gui_demo(request):

    # Denne formular bliver vist på siden
    form = AccelerometerForm()

    # Denne data bliver visualiseret på siden
    N = 10000   # Num samples
    fs = 16000  # Sampling freq
    Ts = 1/fs   # Sampling time
    A = 5       # Amplitude
    f0 = 4000   # Hz

    t = np.linspace(0, N*Ts, N)
    n = np.arange(0, N)
    x = 1.2*A*np.sin(2*np.pi*f0/fs*n) + A*np.sin(2*np.pi*0.75*f0/fs*n) + 0.4*A*np.sin(2*np.pi*1.33*f0/fs*n)

    X = 20*np.log10( np.abs(fft.fft(x, N)) )
    f = fft.fftfreq(N, d=Ts)

    plot = figure(title='FFT powerspektrum😍',
                  sizing_mode='scale_width',
                  x_axis_label='f [Hz]', y_axis_label='|X(f)|^2 [dB]',
                  x_range = [0, fs/2],
                  plot_width=800, toolbar_location="below")

    plot.add_tools(HoverTool())
    plot.line(f, X, legend_label='Powerspektrum for x(t)', color='blue')

    # Her bliver figuren lavet til hhv. JavaScript og indhold til et HTML-div
    script, div = components(plot)

    # Her bliver siden kaldt og variablerne  script, div og form bliver leveret med...
    return render(request, 'demo_module/gui-demo.html', {'script': script, 'div': div, 'form': form})


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

            #------- Temporary saving table ------#
            # save time sent
            temp = ND_TS()
            timestamp = datetime.now()
            temp.TimeStamp = timestamp.strftime("%x-%I:%M:%S")
            temp.ID = 0

            # save no delete field
            temp.NoDelete = form.cleaned_data.get("no_delete")
            temp.save()
            # ------- -------------------- ------#

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
    Janus, March 2020
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


# show running test page will include webcam feed
def demo_running_test(request):
    #Not done
    return render(request, 'demo_module/running_test.html')


# Show specific data page, specific datapoints from a test from saved_data
class show_data(ListView):
    #model = Result  [new result database is "Inbound_teststand_package"]
    template_name = 'demo_module/show_data.html'


#All saved tests
class ResultListView(ListView):
    model = Inbound_teststand_package
    queryset = Inbound_teststand_package.objects.all().order_by('-Timestamp')


#Info page about the demo module
class StatusListView(ListView):
    model = Status
    queryset = Status.objects.all()


# busy page, test already running
def demo_busy(request):
    return render(request, 'demo_module/busy.html')


# Streaming page demo
def demo_stream(request):
    """
    This view must fetch the relevant streaming address and
    insert it into the tempate
    """

    # Get the DK cam settings from the Django settings file
    cam1 = settings.CAMS['cam1']
    cam1.update({
        'activate': request.build_absolute_uri(cam1['api_activate']),
        'url' : request.build_absolute_uri(cam1['api_url'])
    })

    # Get the Japan cam settings from the Django settings file
    cam2 = settings.CAMS['cam2']
    cam2.update({
        'activate': request.build_absolute_uri(cam2['api_activate']),
        'url' : request.build_absolute_uri(cam2['api_url'])
    })

    context = {'cam1': cam1, 'cam2': cam2}
    return render(request, 'demo_module/streaming-demo.html', context)


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
