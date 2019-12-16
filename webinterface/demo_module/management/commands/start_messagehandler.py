from django.core.management.base import BaseCommand
from django.utils import timezone
from demo_module.messagehandler.client import MqttClient
from demo_module.models import Test

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        # define the on_message call-back
        def on_message_callback(client, userdata, message):
            msg = message.payload.decode("utf-8")
            s = Test()
            s.inbound_payload = msg
            s.save()

        # Pass the callback to the client
        subscriber = MqttClient("Listener", on_message_callback)

        # Only subscribe to relevant inbound messages
        subscriber.subscribe("demo_module/inbound")

        print("Starting listening loop")
        subscriber.loop()

