"""View classes for reporter app."""
from rest_framework import generics, viewsets
from reporter.models import IncidentReport, IncidentType
from reporter import serializers
from django.contrib.auth import get_user_model


# Create your views here.
class CreateIncidentReportView(generics.ListCreateAPIView):
    queryset = IncidentReport.objects.all()
    serializer_class = serializers.CreateIncidentReportSerializer


class DetailIncidentReportView(generics.RetrieveUpdateAPIView):
    queryset = IncidentReport.objects.all()
    serializer_class = serializers.CreateIncidentReportSerializer


class IncidentTypesViewset(viewsets.ModelViewSet):
    queryset = IncidentType.objects.all()
    serializer_class = serializers.IncidentTypeSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
