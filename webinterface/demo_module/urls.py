"""
Contains URL routes for the demo_module
All URL paths are <server>/demo_module/<defined_route>

Django 2.2 uses the function path, not url.
"""

from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.demo_home, name='demo_home'),
    path('make_test/', views.demo_make_test, name='demo_make_test'),
    path('show_result/', views.ResultListView.as_view(), name='demo_show_result'),
    path('show_info/', views.StatusListView.as_view(), name='demo_show_info'),
    path('bokeh/', views.bokeh, name='demo_bokeh'),
    #path('send_mqtt', views.send_mqtt, name='demo_send'),
]
