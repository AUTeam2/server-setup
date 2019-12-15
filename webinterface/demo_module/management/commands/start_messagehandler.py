from django.core.management.base import BaseCommand
from django.utils import timezone
from demo_module.messagehandler.client import MqttClient

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)

        team2_subscriber = MqttClient("ListeningForNews")
        team2_subscriber.subscribe("#")
        print("Starting listening loop")
        team2_subscriber.loop()

        #self.stdout.write(s)