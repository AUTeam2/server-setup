"""
Contains URL routes for the demo_module
All URL paths are <server>/demo_module/<defined_route>

Django 2.2 uses the function path, not url.
"""

from django.urls import path
from django.views.generic import TemplateView
from sphinx.testing.path import path

from . import views

urlpatterns = [
    #/demo_module/
    path('',views.demo_main_page,name='demo_home'),

    #/demo_module/start_test/
    path('start_test/',views.demo_create_test,name='demo_make_test'),

    #/demo_module/running_test/
    path('running_test/',views.demo_running_test,name='demo_running_test'),

    #/demo_module/saved_data/
    path('saved_data/',views.ResultListView.as_view(),name='demo_show_result'),

    #/demo_module/saved_data/{test_id}/
    path('saved_data/<pk>/',views.show_data.as_view(),name='demo_specific_data'),

    #/demo_module/info
    path('show_info', views.StatusListView.as_view(), name='demo_show_info'),

    #/demo_module/busy/
    path('busy/',views.demo_busy,name='demo_busy')

    #path for MQTT
    #path('',views.send_mqtt,name='demo_modul')
]
