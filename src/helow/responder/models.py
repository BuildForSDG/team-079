"""Contains responder app model classes."""
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from setup import logger


class Responder(models.Model):
    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)

    location = models.ForeignKey('reporter.Place', on_delete=models.CASCADE, related_name='responder')

    def __str__(self):
        """Returns the string representation of the `Responder` object."""
        return self.name


@receiver(post_save, sender=Responder)
def increment_incident_type_frequency(sender, instance=None, created=False, **kwargs):
    """An observer function that triggers a call to responder once created."""
    if created:
        from responder.views import background_call
        from responder.backgrounders import call_responders

        phone_number = instance.location.international_phone_number
        logger.info(f"Responder: {instance.name} created and assigned to incident: {instance.incident}. Calling "
                    f"responder on: {phone_number}")
        background_call(phone_number)
        logger.info(f"Call to responder: {instance.name} was successful.")
