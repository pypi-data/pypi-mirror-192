from django.contrib import admin
from drf_microservice_auth.models import *


class DrfMicroserviceAuthAdmin(admin.ModelAdmin):
    pass


admin.site.register(MicroserviceUser, DrfMicroserviceAuthAdmin)
admin.site.register(MicroserviceGroup, DrfMicroserviceAuthAdmin)
