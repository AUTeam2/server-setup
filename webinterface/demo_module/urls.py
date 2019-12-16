from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path(
        '',
        views.send_mqtt,
        name='demo_modul',
    ),
]

