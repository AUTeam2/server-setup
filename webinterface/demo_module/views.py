from django.shortcuts import render
from django.http import HttpResponse
from demo_module.messagehandler.client import MqttClient
from demo_module.messagehandler import protocol
from django.template import loader


# remember to implement database import in views, when database gets implemented
# from . models import database_tests, datatypes, datapoints


# Create your views here.

# main demo_module page
def index(request):
    return render(request, '/demo_module/templates/index.html')


# start/create test page
def start_test(request):
    return render(request, '/demo_module/templates/start_test.html')


# show running test page
def running_test(request):
    return render(request, '/demo_module/templates/running_test.html')


# show saved test page
def saved_data(request):
    # import all test, when database is implementet uncomment these
    # all_test = Date_list.objects.all()
    # context = {"all_test" : all_test}
    # return render(request, '/demo_module/templates/saved_data.html',context)
    return render(request, '/demo_module/templates/saved_data.html')


# Show specific data page, specific datapoints from a test from saved_data
def show_data(request, data_id):
    # import specific test data, when database is implementet uncomment these
    # datatype_list = date_list.objects.get(pk= 'primary_key')
    # datapoints = datapoints.objects.filter(collection=datatype_list)
    # context = {"datapoints" : datapoints}
    # return render(request, '/demo_module/templates/show_data.html',context)
    return render(request, '/demo_module/templates/show_data.html', )


# busy page, test already running
def busy(request):
    return render(request, '/demo_module/templates/busy.html')


# mqtt handler
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
        'x': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'y': [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
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
