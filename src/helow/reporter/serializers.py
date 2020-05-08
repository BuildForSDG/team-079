"""The serializer class for all endpoints."""
from rest_framework import serializers
from reporter.models import IncidentReport, IncidentLocation, IncidentType
from django.contrib.auth import get_user_model
from responder.serializers import ResponderSerializer


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)


class IncidentLocationSerializer(serializers.ModelSerializer):
    """Serializer for location model."""

    class Meta:
        model = IncidentLocation
        fields = ('id', 'name', 'latitude', 'longitude')


class IncidentTypeSerializer(serializers.Serializer):
    """IncidentType Serializer"""
    id = serializers.IntegerField()
    label = serializers.CharField(required=False)
    frequency = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return IncidentType.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.label = validated_data.get('label', instance.label)
        instance.frequency = validated_data.get('frequency', instance.frequency)
        instance.save()
        return instance


class CreateIncidentReportSerializer(serializers.Serializer):
    """Model serializer for `IncidentReport`."""
    id = serializers.PrimaryKeyRelatedField(queryset=IncidentReport.objects.all(), required=False)
    title = serializers.CharField(max_length=50)
    description = serializers.CharField(max_length=200)
    reported_by = UserSerializer(required=False)
    reported_at = serializers.DateTimeField()
    incident_type = IncidentTypeSerializer()
    responder = ResponderSerializer(required=False)
    is_status_open = serializers.BooleanField(required=False)
    location = IncidentLocationSerializer()

    def create(self, validated_data):
        """Create and return a new `IncidentReport` instance, given the validated data."""
        # get user object if user is not anonymous
        user_data = validated_data.get('reported_by')
        if user_data:
            user = get_user_model().objects.get(**user_data)[0]
            validated_data['reported_by'] = user

        # get the incident type object with the provided id
        incident_type_data = validated_data.get('incident_type')
        if incident_type_data:
            incident_type = IncidentType.objects.get(id=incident_type_data.get('id'))
            validated_data['incident_type'] = incident_type

        # create a location for this incident
        location_data = validated_data.pop('location')
        location = IncidentLocation.objects.create(**location_data)

        # create this incident
        return IncidentReport.objects.create(location=location, **validated_data)


