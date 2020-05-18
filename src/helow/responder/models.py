"""Contains responder app model classes."""
from django.db import models


# Create your models here.
class Responder(models.Model):
    name = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)

    location = models.ForeignKey('reporter.IncidentLocation', on_delete=models.CASCADE, related_name='responder')

    def __str__(self):
        """Returns the string representation of the `Responder` object."""
        return self.name
