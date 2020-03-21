"""
This is a management command, that listens for inbound messages.
This module is responsible for storing inbound status messages and data messages.

This module implements B41.
Design is documented in B36-B38.
Uses the B39 JSON schema, which implements the protocol v1.0.
"""

from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from demo_module.messagehandler.client import MqttClient
from demo_module.messagehandler import protocol
from demo_module.models import Status, Inbound_teststand_package, Test_stand_data, Test_stand_parameters
from demo_module.models import ND_TS


# for database structure
class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        # define the on_message call-back
        def on_message_callback(client, userdata, message):

            # Create a new message object
            m = protocol.Message()

            # Convert the incoming JSON message to Python vars
            msg = message.payload.decode("utf-8")
            obj = protocol.ProtocolSchema.read_jsonstr(msg)

            # Do some validation here
            # Evaluate if the Python object conforms to the protocol
            schema_validation_result = protocol.ProtocolSchema.validating(obj, m.protocol_schema)

            # If validation fails it will give a boolean fail in the database, and skip the unpacking process
            if schema_validation_result == True:

                # Insert into struct-like variables in the m-object.
                m.unpack(**obj)
                package = obj

                # Store any received statuscodes
                # 6xx -> Power Codes
                # 1xx-5xx -> Status Codes
                if m.msgType == "status":
                    # Get object in the db
                    s = Status()
                    s.ID = 0

                    if int(m.statusCode) >= 600:
                        s.latest_power_code = m.statusCode
                    else:
                        s.latest_status_code = m.statusCode

                    # Update the object
                    s.save()

                # For inbound data
                if m.msgType == "data":

                    # Create and store a JSON package in the db
                    ITP = Inbound_teststand_package()

                    # TimeStamp and nodelete copied from temporary model
                    temp = ND_TS.objects.all()[0]
                    ITP.Timestamp = temp.TimeStamp
                    ITP.NODELETE = temp.NoDelete

                    # Store values from inbound validated JSON
                    ITP.Sent_by = package["sentBy"]
                    ITP.command_list = package["commandList"]
                    ITP.Validation_failed = 0
                    ITP.save()

                    # Parameter's table
                    for p_name, p_val in package["parameterObj"].items():
                        print(p_name, p_val)
                        TSP = Test_stand_parameters()
                        TSP.Parameter_name = p_name
                        TSP.Parameter_value = p_val
                        TSP.Inbound_teststand_package = ITP
                        TSP.save()

                    # Data table
                    for data_name, data_points in package["dataObj"].items():
                        print(data_name, data_points)
                        TSD = Test_stand_data()
                        TSD.Data_name = data_name
                        TSD.Data_points = data_points
                        TSD.Inbound_teststand_package = ITP
                        TSD.save()

            else:
                package = obj

                # Create and store a JSON package in the db
                ITP = Inbound_teststand_package()

                # TimeStamp
                Timestamp = datetime.now()

                if "sentBy" in package:
                    ITP.Sent_by = package["sentBy"]
                else:
                    ITP.Sent_by = "Failed validation"

                ITP.Timestamp = Timestamp.strftime("%x-%I:%M:%S")
                ITP.Validation_failed = 1

                ITP.save()

        # Pass the callback to the client
        subscriber = MqttClient("MessageHandler", on_message_callback)

        # Only subscribe to relevant inbound messages
        subscriber.subscribe("demo_module/inbound")

        print("Starting listening loop")
        subscriber.loop()
