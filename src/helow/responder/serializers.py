"""Model serializers for responder app."""
from rest_framework import serializers
from .models import Responder


class ResponderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Responder
        fields = ('id', 'name', 'industry')
