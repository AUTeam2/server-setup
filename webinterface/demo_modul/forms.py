from django import forms
from .models import Accelerator

# Forms have been used to make get/post request easier to handle
class Accelerator(forms.ModelForm):


    # Meta class have been added to associate the form "testForm" with the model "Testdatabase"
    class Meta:
        model = Accelerator
        fields = ['Data', 'NODELETE', 'Sensor_chosen']