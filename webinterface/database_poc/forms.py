from django import forms
from .models import Testdatabase

# Forms have been used to make get/post request easier to handle
class TestForm(forms.ModelForm):
    Data = forms.CharField()
    NODELETE = forms.CheckboxInput()

    # Meta class have been added to associate the form "testForm" with the model "Testdatabase"
    class Meta:
        model = Testdatabase
        fields = ('Data', 'NODELETE',)
        attrs = {
            'class': 'form-control'
        }