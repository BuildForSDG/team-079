"""Model classes for the presenter app."""
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class IncidentType(models.Model):
    """Model class to handle all incident types."""
    label = models.CharField(max_length=50, null=False)
    frequency = models.IntegerField(null=False, default=0)

    def __str__(self):
        return self.label


class Location(models.Model):
    """Model class to handle all incident's location."""
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)

    def __str__(self):
        return f"latitude: {self.latitude}, longitude: {self.longitude}"


class IncidentReport(models.Model):
    """Model class to handle incident reports."""
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    reported_at = models.DateTimeField()
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=2)
    incident_type = models.ForeignKey(IncidentType, on_delete=models.CASCADE, default=1)
    is_status_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title
