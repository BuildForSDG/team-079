"""Model serializers for responder app."""
from rest_framework import serializers
from .models import Responder


class ResponderSerializer(serializers.ModelSerializer):
    """`Responder` serializer class."""

    class Meta:
        model = Responder
        fields = ('id', 'name', 'industry')
