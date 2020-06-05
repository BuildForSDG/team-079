"""Model classes for the presenter app."""
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from config import Config as config


# Create your models here.
class IncidentType(models.Model):
    """Model class to handle all incident types."""

    label = models.CharField(max_length=50, null=False)
    frequency = models.IntegerField(null=False, default=0)

    def __str__(self):
        """Returns the string representation of the `IncidentType` object."""
        return self.label


class Place(models.Model):
    """Model class to handle all locations."""

    map_name = models.CharField(max_length=200, null=False)
    known_name = models.CharField(max_length=200, null=True)
    place_id = models.CharField(max_length=200, null=True)
    formatted_address = models.CharField(max_length=200, null=True)
    formatted_phone_number = models.CharField(max_length=20, null=True)
    international_phone_number = models.CharField(max_length=20, null=True)
    location_lat = models.FloatField(null=False)
    location_lng = models.FloatField(null=False)
    viewport_ne_lat = models.FloatField(null=True)
    viewport_ne_lng = models.FloatField(null=True)
    viewport_sw_lat = models.FloatField(null=True)
    viewport_sw_lng = models.FloatField(null=True)
    rating = models.FloatField(null=True)
    vicinity = models.CharField(max_length=200, null=True)
    url = models.CharField(max_length=200, null=True)
    website = models.CharField(max_length=100, null=True)
    owner = models.CharField(max_length=20, null=True)

    def __str__(self):
        """Returns the string representation of the `Place` object."""
        name = self.known_name if self.map_name is None else self.map_name
        return name


class IncidentReport(models.Model):
    """Model class to handle incident reports."""

    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=False)
    location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='incidents')
    reported_at = models.DateTimeField()
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=config.ANONYMOUS_USER_ID)
    incident_type = models.ForeignKey(IncidentType, on_delete=models.CASCADE, default=config.UNCATEGORIZED_REPORT_ID)
    responder = models.ForeignKey('responder.Responder', on_delete=models.CASCADE, null=True, related_name='incidents')
    status = models.CharField(max_length=50, default=config.STATUS_PENDING)

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




