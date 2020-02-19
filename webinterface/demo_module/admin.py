from django.contrib import admin
from .models import Status, Result, Test

# Register your models here.
admin.site.register(Status)
admin.site.register(Result)
admin.site.register(Test)