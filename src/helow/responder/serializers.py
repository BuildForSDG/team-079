"""Model serializers for responder app."""
from rest_framework import serializers
from .models import Responder


class ResponderSerializer(serializers.ModelSerializer):
    """`Responder` serializer class."""
    import reporter.serializers as se
    location = se.IncidentLocationSerializer()

    class Meta:
        model = Responder
        fields = '__all__'
