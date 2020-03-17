from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Status(models.Model):
    class Meta:
        verbose_name_plural = "Status"

    """
    Status contains the inbound synchronization table.
    Documented in B36, B37, B38.
    Status codes 1xx-5xx are stored in latest_status_code
    Power states 6xx are stored in power_state
    """

    STATUS_CODES = [
        ('200', '200 OK'),
        ('202', '202 Received and accepted'),
        ('400', '400 Bad request'),
        ('404', '404 Not found'),
        ('405', '405 Method not allowed'),
        ('500', '500 Internal error on device'),
    ]

    POWER_CODES = [
        ('600', '600 Device on'),
        ('610', '610 Device in hibernation'),
        ('620', '620 Device off'),
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
    def hard_reset_to_ready(cls):
        """
        This function is only  run once.
        Hard initialization to Ready status, e.g. if a test-stand has not before reported status.
        """
        if not (cls.objects.exists()):
            s = Status()
            s.latest_status_code = '200'
            s.latest_power_code = '620'
            s.save()                        # save a new row

    def __str__(self):
        return f"Latest Status Code: {self.latest_status_code}, Latest Power Code: {self.latest_power_code}."


class Result(models.Model):
    """
    Result creates a model and table with results.
    Used for storing inbound results from a test-stand
    Design documented in B36, B37, B38.
    Protocol documented in LaunchPhase doc. ver. 1
    """

    # Who initiated the test (username or similar), when were results received
    job_requested_by = models.CharField(max_length=100)
    job_received_time = models.DateTimeField(auto_now='True')

    # Set to true if this is important data not to be cleaned up
    job_NODELETE = models.BooleanField(default=False)

    # Value fields from protocol v1.0

    # Array of commands (textual), each no longer than 20 chars
    command_list = ArrayField(
        models.CharField(max_length=20)
    )

    # The contents of this object is defined by the test-stand implementers
    # Meant to transfer settings/parameters for a test
    parameter_obj = JSONField()

    # The contents of this object is defined by the test-stand implementers
    # Meant to transfer data, such as comma-separated values from a test
    data_obj = JSONField()

    # Define the filetype that is embedded in the JSON as binary data
    # Prefer to use MIME types here
    embedded_file_format = models.CharField(max_length=20)

    # File embedded in JSON as raw binary data
    embedded_file = models.BinaryField()


class Test(models.Model):
    """
    This model is only for testing the ability of the MQTT Client.
    The entire inbound payload will be saved to the single field.
    """

    inbound_payload = JSONField()


class Test2(models.Model):
    """
    This model is only for testing the ability of the MQTT Client.
    The entire inbound payload will be saved to the single field.
    """

    inbound_payload = JSONField()


# ---------------- database package structure ---------------- #
# [Inbound_teststand_package]
#                         |_ [Test_stand_data]
#                         |_ [Test_stand_parameter]
# [ND_TS]


# Primary table
class Inbound_teststand_package(models.Model):
    class Meta:
        verbose_name_plural = "Teststand packages"

    Timestamp = models.CharField(max_length=200, null=True, blank=True)
    NODELETE = models.BooleanField(default=False)
    Sent_by = models.CharField(max_length=200)
    command_list = ArrayField(models.CharField(max_length=20), null=True, blank=True)
    Validation_failed = models.BooleanField(default=True)

    def __str__(self):
        return self.Timestamp

# Secondary table [data]
class Test_stand_data(models.Model):
    class Meta:
        verbose_name_plural = "Teststand data types"

    Data_name = models.CharField(max_length=100, null=True)
    Data_points = JSONField(blank=True, null=True)
    Inbound_teststand_package = models.ForeignKey(Inbound_teststand_package, on_delete=models.CASCADE,
                                                  related_name='data')

    def __str__(self):
        return '{} - {}'.format(self.Inbound_teststand_package, self.Data_name)

# Secondary table [parameters]
class Test_stand_parameters(models.Model):
    class Meta:
        verbose_name_plural = "Teststand parameters"

    Parameter_name = models.CharField(max_length=100, default="Empty")
    Parameter_value = models.CharField(max_length=100, default="Empty")
    Inbound_teststand_package = models.ForeignKey(Inbound_teststand_package, on_delete=models.CASCADE,
                                                  related_name='parameters')

    def __str__(self):
        return '{} - {}'.format(self.Inbound_teststand_package, self.Parameter_name)


# Temporary table for no delete and timestamp
# Gets values when test is started from "view.py"
# Passes values to primary table, when test is inbound from "start_messagehandler.py"
class ND_TS(models.Model):
    class Meta:
        verbose_name_plural = "NoDelete & TimeStamp"

    ID = models.IntegerField(primary_key=True)
    TimeStamp = models.CharField(max_length=200, null=True, blank=True)
    NoDelete = models.BooleanField(default=False)
    StatusCode = models.CharField(max_length=50, default="empty")


    def __str__(self):
        return self.TimeStamp
