from django.http import HttpResponse
from rest_framework import generics
from reporter.models import IncidentReport, Location
from api import serializers


# Create your views here.
class CreateIncidentReportView(generics.ListCreateAPIView):
    queryset = IncidentReport.objects.all()
    serializer_class = serializers.IncidentReportSerializer


class DetailIncidentReportView(generics.RetrieveUpdateAPIView):
    queryset = IncidentReport.objects.all()
    serializer_class = serializers.IncidentReportSerializer

