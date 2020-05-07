"""The serializer class for all endpoints."""
from rest_framework import serializers
from reporter.models import IncidentReport, Location, IncidentType
from django.contrib.auth import get_user_model


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=100, required=False)


class IncidentLocationSerializer(serializers.Serializer):
    """Serializer for location model."""
    id = serializers.IntegerField(required=False)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()

    def create(self, validated_data):
        """
        Create and return a new `Location` instance, given the validated data.
        """
        return Location.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Location` instance, given the validated data.
        """
        instance.name = validated_data.get('latitude', instance.latitude)
        instance.email = validated_data.get('longitude', instance.longitude)
        instance.save()
        return instance


class IncidentTypeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    label = serializers.CharField(max_length=50, required=False)

    def create(self, validated_data):
        """Create and return a new `IncidentType` instance, given the validated data."""
        return IncidentType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update and return an existing `IncidentType` instance, given the validated data."""
        instance.name = validated_data.get('label', instance.label)
        instance.save()
        return instance


class IncidentReportSerializer(serializers.Serializer):
    """Model serializer for `IncidentReport`."""
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    location = IncidentLocationSerializer()
    reported_at = serializers.DateTimeField()
    incident_type = IncidentTypeSerializer()
    is_status_open = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """Create and return a new `IncidentReport` instance, given the validated data."""
        location_data = validated_data.pop('location', None)
        if location_data:
            location = Location.objects.get_or_create(**location_data)[0]
            validated_data['location'] = location

        user_data = validated_data.pop('reported_by', None)
        if user_data:
            user = get_user_model().objects.get(**location_data)[0]
            validated_data['reported_by'] = user

        incident_type_data = validated_data.pop('incident_type', None)
        if incident_type_data:
            incident_type = IncidentType.objects.get(id=incident_type_data.get('id'))
            validated_data['incident_type'] = incident_type
        return IncidentReport.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Updates an existing `IncidentReport`."""
        location_data = validated_data.pop('location')
        location = instance.location

        instance.username = validated_data.get('latitude', instance.latitude)
        instance.email = validated_data.get('longitude', instance.longitude)
        instance.save()

        return instance

