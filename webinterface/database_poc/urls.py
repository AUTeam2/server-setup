from django.urls import path
from . import views

# The URL paths which belongs to this app and which "view" that is gonna be shown on the specific URL
urlpatterns = [
    # URL/test/
    path('', views.testpage.as_view(), name='test'),

    # URL/test/datainput
    path('datainput/', views.datainput.as_view(), name='datainput'),

    # URL/test/dataoutput
    path('dataoutput/', views.dataoutput.as_view(), name='dataoutput')
]