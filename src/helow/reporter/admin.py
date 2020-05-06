from django.contrib import admin
from reporter import models

# Register your models here.
admin.site.register(models.IncidentType)
admin.site.register(models.Location)
admin.site.register(models.IncidentReport)
