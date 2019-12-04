from django.db import models

# create your models here:
class Testdatabase(models.Model):
    # In case that the models is changes remember to use the command "python manage.py make migration"
    Data = models.CharField(max_length=100)
    Timestamp = models.DateTimeField(auto_now='True')
    NODELETE = models.BooleanField(default=False)

    # Returns if the class is called as a function
    def __str__(self):
        return self.Data


