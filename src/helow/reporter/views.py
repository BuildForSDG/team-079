"""View classes for reporter app."""
from rest_framework import generics, viewsets
from reporter.models import IncidentReport, IncidentType
from reporter import serializers


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
