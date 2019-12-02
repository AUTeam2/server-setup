from django.db import models

# create your models here:

# In case that the models is changes remember to use the command "python manage.py make migration"
class Accelerator(models.Model):

    sensor1 = 's1'
    sensor2 = 's2'
    sensor3 = 's3'
    sensors = (
        (sensor1, 'sensor1'),
        (sensor2, 'sensor2'),
        (sensor3, 'sensor3')
    )

    Sensor_chosen = models.CharField(max_length=20, choices=sensors , default=sensor1)
    Data = models.CharField(max_length=10000)
    Timestamp = models.DateTimeField(auto_now='True')
    NODELETE = models.BooleanField(default=False)

    # Returns if the class is called as a function
    def __str__(self):
        return self.Data

class Aktuator(models.Model):

    Data = models.CharField(max_length=10000)
    Timestamp = models.DateTimeField(auto_now='True')
    NODELETE = models.BooleanField(default=False)