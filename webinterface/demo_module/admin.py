from django.contrib import admin
from .models import Status, Result, Test

# Register your models here.
#@admin.register(Result)
admin.site.register(Result)
class ResultAdmin(admin.ModelAdmin):
    readonly_fields = ['job_received_time']
    fields = ['job_NODELETE', 'command_list', 'parameter_obj', 'data_obj']
    date_hierarchy = 'job_received_time'


admin.site.register(Status)
admin.site.register(Test)