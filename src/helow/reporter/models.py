"""Model classes for the presenter app."""
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from responder.models import Responder


# Create your models here.
class IncidentType(models.Model):
    """Model class to handle all incident types."""

    label = models.CharField(max_length=50, null=False)
    frequency = models.IntegerField(null=False, default=0)

    def __str__(self):
        """Returns the string representation of the `IncidentType` object."""
        return self.label


class IncidentLocation(models.Model):
    """Model class to handle all incident's location."""

    name = models.CharField(max_length=100, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)

    def __str__(self):
        """Returns the string representation of the `IncidentLocation` object."""
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
        """Returns the string representation of the `IncidentReport` object."""
        return self.title


@receiver(post_save, sender=IncidentReport)
def increment_incident_type_frequency(sender, instance=None, created=False, **kwargs):
    if created:
        # get the incident type object and increment its type
        incident_type = instance.incident_type
        incident_type.frequency = incident_type.frequency + 1
        incident_type.save()
