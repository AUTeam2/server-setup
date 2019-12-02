from django.shortcuts import render, redirect
from .models import Accelerator
from .forms import Accelerator
from django.views import View

# Create your views here.

#/demo_modul/input    (should become start test at a later point, but for now it's for app testing)
class module_homepage(View):

    # get request to load the webpage, where the "form" TestForm defines the textfield and the tick box
    def get(self, request):
        form = Accelerator()
        return render(request, 'app_Template/demo_modul_homepage.html', {'form':form})

    # The post request which activates when the "submit" button is pressed
    def post(self, request):
        form = Accelerator(request.POST)

        # Saves the input if the input is valid
        if form.is_valid():
            form.save()
            return redirect('/test/')

        # In case of an invalid statement such as a blank textfield
        return render(request, 'app_Template/demo_modul_hompepage.html', {'form':form})

#/demo_modul/results
class results(View):

    # The get request which loads the web page, which gets the objects from the database to be shown.
    def get(self, request):
        all_data = Accelerator.objects.all()
        return render(request, 'app_Template/result_page.html', {'all_data': all_data})