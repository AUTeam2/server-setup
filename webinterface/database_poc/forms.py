from django import forms
from .models import testdatabase

# Forms have been used to make get/post request easier to handle
class TestForm(forms.ModelForm):
    Data = forms.CharField()
    NODELETE = forms.CheckboxInput()

    # Meta class have been added to associate the form "testForm" with the model "testdatabase"
    class Meta:
        model = testdatabase
        fields = ('Data', 'NODELETE',)