"""Model classes for the presenter app."""
from django.db import models
from django.contrib.auth import get_user_model
from responder.models import Responder


# Create your models here.
class IncidentType(models.Model):
    """Model class to handle all incident types."""
    label = models.CharField(max_length=50, null=False)
    frequency = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.label


class IncidentLocation(models.Model):
    """Model class to handle all incident's location."""
    name = models.CharField(max_length=100, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)

    def __str__(self):
        return f" name: {self.name}, latitude: {self.latitude}, longitude: {self.longitude}"


class IncidentReport(models.Model):
    """Model class to handle incident reports."""
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=False)
    location = models.ForeignKey(IncidentLocation, on_delete=models.CASCADE, related_name='incidents')
    reported_at = models.DateTimeField()
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=2)
    incident_type = models.ForeignKey(IncidentType, on_delete=models.CASCADE, default=1)
    responder = models.ForeignKey(Responder, on_delete=models.CASCADE, null=True)
    is_status_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title

