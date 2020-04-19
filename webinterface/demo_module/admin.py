from django.contrib import admin
from .models import Status, Result, Test, Inbound_teststand_package, Test_stand_parameters, Test_stand_data, ND_TS

# Register your models here.
#@admin.register(Result)
admin.site.register(Result)
class ResultAdmin(admin.ModelAdmin):
    readonly_fields = ['job_received_time']
    fields = ['job_NODELETE', 'command_list', 'parameter_obj', 'data_obj']
    date_hierarchy = 'job_received_time'


admin.site.register(Status)
admin.site.register(Test)
admin.site.register(Inbound_teststand_package)
admin.site.register(Test_stand_data)
admin.site.register(Test_stand_parameters)
admin.site.register(ND_TS)