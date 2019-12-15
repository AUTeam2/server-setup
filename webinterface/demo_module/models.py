from django.db import models
import time

# Create your models here.

class Status(models.Model):
    """
    Status implements the inbound synchronization.
    Documented in B36, B37, B38.
    Status codes 1xx-5xx are stored in latest_status_code
    Power states 6xx are stored in power_state
    """

    STATUS_CODES = [
        ('200', 'OK'),
        ('202', 'Received and accepted'),
        ('400', 'Bad request'),
        ('404', 'Not found'),
        ('405', 'Method not allowed'),
        ('500', 'Internal error on device'),
    ]

    POWER_CODES = [
        ('600', 'Device on'),
        ('610', 'Device in hibernation'),
        ('620', 'Device off'),
    ]

    latest_status_code = models.CharField(max_length=3, choices=STATUS_CODES, default='200')
    latest_status_update = models.DateTimeField(auto_now='True')

    latest_power_code = models.CharField(max_length=3, choices=POWER_CODES, default='620')
    latest_power_update = models.DateTimeField(auto_now='True')

    @classmethod
    def ready(cls):
        """
        Implements check to see if device is ready
        """
        status = cls.objects.all()[0].latest_status_code
        power = cls.objects.all()[0].latest_power_code

        if (status == '200') and (power == '600'):
            return True
        else:
            return False

    @classmethod
    def initialize_if_empty(cls):
        """
        This function should only be run once.
        Initializes the Status table if a teststand has never before reported status.
        """
        if not (cls.objects.exists()):
            s = Status()
            s.latest_status_code = '200'
            s.latest_power_code = '620'
            s.save()                        # save a new row