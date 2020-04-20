"""
Contains URL routes for the test_module
All URL paths are <server>/test_module/<defined_route>

Django 2.2 uses the function path, not url.
"""

from django.urls import path
from django.views.generic import TemplateView


from . import views

urlpatterns = [
    #/test_module/
    path('',views.test_main_page,name='test_home'),

    #/test_module/start_test/
    path('start_test/',views.test_create_test,name='test_make_test'),

    #/test_module/running_test/
    path('running_test/',views.test_running_test,name='test_running_test'),

    #/test_module/saved_data/
    path('saved_data/',views.ResultListView.as_view(),name='test_show_result'),

    #/test_module/saved_data/{test_id}/  <- Show only this dataset
    path('saved_data/<int:test_id>/', views.show_data,name='test_specific_data'),

    # /test_module/saved_data/csv/{test_id}  <- spit out a CSV-file for this
    path('saved_data/csv/<int:test_id>/', views.make_csv_from_db, name='test_csv'),

    # /test_module/saved_data/excel/{test_id}  <- spit out a excel-file for this
    path('saved_data/excel/<int:test_id>/', views.make_excel_from_db, name='test_excel'),

    # /test_module/info
    path('show_info', views.StatusListView.as_view(), name='test_show_info'),

    # Show various GUI elements
    path('gui_test/', views.gui_test, name='test_gui'),

    # Show webcam test
    path('stream/', views.test_stream, name='test_stream'),

    # Below here must be fully implemented

    #/test_module/busy/
    path('busy/',views.test_busy,name='test_busy'),


    #path for MQTT
    #path('',views.send_mqtt,name='test_modul')
]
