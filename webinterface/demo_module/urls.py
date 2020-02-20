from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.demo_home, name='demo_home'),
    path('send_mqtt', views.send_mqtt, name='demo_send'),
]

