from django.contrib import admin
from .models import Client, ServiceProvider, ServiceRecords
# Register your models here.
admin.site.register(Client)
admin.site.register(ServiceProvider)
admin.site.register(ServiceRecords)