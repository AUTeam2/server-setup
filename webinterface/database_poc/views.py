from django.shortcuts import render, redirect
from .models import Testdatabase
from .forms import TestForm
from django.views import View

# Create your views here.
#/test/
class testpage(View):

    def get(self, request):
        return render(request, 'database_poc/test.html')

#/test/datainput/
class datainput(View):

    # get request to load the webpage, where the "form" TestForm defines the textfield and the tick box
    def get(self, request):
        form = TestForm()
        return render(request, 'database_poc/datainput.html', {'form':form})

    # The post request which activates when the "submit" button is pressed
    def post(self, request):
        form = TestForm(request.POST)

        # Saves the input if the input is valid
        if form.is_valid():
            form.save()
            return redirect('/test/')

        # In case of an invalid statement such as a blank textfield
        return render(request, 'database_poc/datainput.html', {'form':form})

class dataoutput(View):

    # The get request which loads the web page, which gets the objects from the database to be shown.
    def get(self, request):
        all_data = Testdatabase.objects.all()
        return render(request, 'database_poc/dataoutput.html', {'all_data': all_data})