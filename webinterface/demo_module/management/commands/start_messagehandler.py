"""
This is a management command, that listens for inbound messages.
This module is responsible for storing inbound status messages and data messages.

This module implements B41.
Design is documented in B36-B38.
Uses the B39 JSON schema, which implements the protocol v1.0.
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from demo_module.messagehandler.client import MqttClient
from demo_module.messagehandler import protocol
from demo_module.models import Status, Result, Test

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        # define the on_message call-back
        def on_message_callback(client, userdata, message):

            #Create a new message object
            m = protocol.Message()

            # Do some validation here
            # TO DO...

            # Convert the incoming JSON message to Python vars
            msg = message.payload.decode("utf-8")
            obj = protocol.ProtocolSchema.read_jsonstr(msg)
            m.unpack(**obj)

            # Store any received statuscodes
            # 6xx -> Power Codes
            # 1xx-5xx -> Status Codes
            if m.msgType == "status":
                # Get object in the db
                s = Status.objects.all()[0]

                if int(m.statusCode) >= 600:
                    s.latest_power_code = m.statusCode
                else:
                    s.latest_status_code = m.statusCode

                # Update the object
                s.save()

            if m.msgType == "data":
                # Create and store a new result in the db
                r = Result()

                # Needs to be decided:
                # - How to transport the nodelete tag through a roundtrip?
                # - How to transport the requested_by tag through a roundtrip?
                # - Is it the right choice to store the embedded file as binary? Do we need it?

                # Set relevant values from message
                r.command_list = m.commandList
                r.parameter_obj = m.parameterObj
                r.data_obj = m.dataObj
                r.embedded_file_format = m.embeddedFileFormat
                r.embedded_file = bytearray(m.embeddedFile, "utf8")

                # Create the object in the db
                r.save()

        # Pass the callback to the client
        subscriber = MqttClient("MessageHandler", on_message_callback)

        # Only subscribe to relevant inbound messages
        subscriber.subscribe("demo_module/inbound")

        print("Starting listening loop")
        subscriber.loop()