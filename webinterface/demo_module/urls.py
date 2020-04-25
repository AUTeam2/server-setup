"""
Contains URL routes for the demo_module
All URL paths are <server>/demo_module/<defined_route>

Django 2.2 uses the function path, not url.
"""

from django.urls import path
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    #/demo_module/
    path('',views.demo_main_page,name='demo_home'),

    #/demo_module/start_test/
    path('start_test/',views.demo_create_test,name='demo_make_test'),

    #/demo_module/test middle link
    path('test_middle_link/', views.demo_create_test_middle_link,name='demo_middle_link'),

    #/demo_module/running_test/
    path('running_test/',views.demo_running_test,name='demo_running_test'),

    #/demo_module/saved_data/
    path('saved_data/',views.ResultListView.as_view(),name='demo_show_result'),

    #/demo_module/saved_data/{test_id}/  <- Show only this dataset
    path('saved_data/<int:test_id>/', views.show_data,name='demo_specific_data'),

    # /demo_module/saved_data/csv/{test_id}  <- spit out a CSV-file for this
    path('saved_data/csv/<int:test_id>/', views.make_csv_from_db, name='demo_csv'),

    # /demo_module/saved_data/excel/{test_id}  <- spit out a excel-file for this
    path('saved_data/excel/<int:test_id>/', views.make_excel_from_db, name='demo_excel'),

    # /demo_module/info
    path('show_info', views.StatusListView.as_view(), name='demo_show_info'),

    # Show various GUI elements
    path('gui_demo/', views.gui_demo, name='demo_gui'),

    # Show webcam demo
    path('stream/', views.demo_stream, name='demo_stream'),

    # Below here must be fully implemented

    #/demo_module/busy/
    path('busy/',views.demo_busy,name='demo_busy'),


    #path for MQTT
    #path('',views.send_mqtt,name='demo_modul')
]
