"""
This is a management command, that listens for inbound messages.
This module is responsible for storing inbound status messages and data messages.
"""

from comms.messagehandler import protocol
from comms.messagehandler.client import MqttClient
from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

# Get values from settings file
subscriptions = settings.MESSAGE_SUBSCRIPTIONS

# for database structure
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting MessageHandler")

        def on_publish_callback(client, userdata, mid):
            pass

        # define the on_message call-back
        def on_message_callback(client, userdata, message):
            msg = message.payload.decode("utf-8")
            topic = message.topic
            topic_parts = topic.split('/') #consider matching using regex instead
            handler_module = topic_parts[settings.GET_TOPIC_COMPONENT] # looks up -> 'demo_module' or similar

            try:
                # Find the settings for callback handling for this module
                callbacks = settings.MESSAGE_CALLBACKS[handler_module]
            except KeyError:
                print("The topic is not registered with a handler in settings.py")
                return False

            # Get access to the handler's functions
            app = apps.get_app_config(handler_module)
            models_module = app.models_module

            # Create a new message object, Convert the incoming JSON message
            m = protocol.Message()
            obj = protocol.ProtocolSchema.read_jsonstr(msg)

            # Do validation: Evaluate if the Python object conforms to the protocol
            schema_validation_result = protocol.ProtocolSchema.validating(obj, m.protocol_schema)

            # If validation fails it will give a boolean fail in the database, and skip the unpacking process
            if schema_validation_result:

                # Insert into struct-like variables in the message-object.
                m.unpack(**obj)

                if m.msgType == "status":
                    # Get at function pointer for updating status
                    func = getattr(models_module, callbacks['status_callback'])

                    # Call the desired function, pass the message
                    func(m)

                # For inbound data
                if m.msgType == "data":
                    # Get at function pointer for inbound data
                    func = getattr(models_module, callbacks['data_callback'])

                    # Call the desired function, pass the message
                    func(m)

            else:
                # Get at function pointer for fallback handler
                func = getattr(models_module, callbacks['fallback_callback'])

                # Call the desired function, pass the message
                func(m)

        # Pass the callback to the client
        subscriber = MqttClient("MessageHandler", on_message_callback, on_publish_callback)

        # Only subscribe to relevant inbound messages
        subscriber.subscribe(subscriptions)

        print("Starting listening loop")
        subscriber.loop()
