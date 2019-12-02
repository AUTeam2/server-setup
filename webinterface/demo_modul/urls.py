from django.urls import path
from . import views

# The URL paths which belongs to this app and which "view" that is gonna be shown on the specific URL
urlpatterns = [
    # URL/module_homepage/
    path('', views.module_homepage.as_view(), name='module_homepage'),

    # URL/module_homepage/results
    path('results/', views.results.as_view(), name='results')
]