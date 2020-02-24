from django.urls import path
from django.views.generic import TemplateView
from sphinx.testing.path import path

from . import views

urlpatterns = [

    #/demo_module/
    path('/',views.index,name='index'),

    #/demo_module/start_test/
    path('/start_test/',views.start_test,name='start_test'),

    #/demo_module/running_test/
    path('/running_test/',views.running_test,name='running_test'),

    #/demo_module/saved_data/
    path('/saved_data/',views.saved_data,name='saved_data'),

    #/demo_module/{test_id}/
    path('</int:data_id>',views.show_data,name='show_data'),

    #/demo_module/busy/
    path('/busy/',views.busy,name='busy'),

    #path for MQTT
    path(
        '',
        views.send_mqtt,
        name='demo_modul',
    )
]

