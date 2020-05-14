"""View classes for reporter app."""
from rest_framework import generics
from reporter.models import IncidentReport
from reporter import serializers
from rest_framework.pagination import PageNumberPagination
# from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter


# Create your views here.
class CreateIncidentReportView(generics.ListCreateAPIView):
    queryset = IncidentReport.objects.all()
    serializer_class = serializers.CreateIncidentReportSerializer


class DetailIncidentReportView(generics.RetrieveUpdateAPIView):
    queryset = IncidentReport.objects.all()
    serializer_class = serializers.CreateIncidentReportSerializer


class IncidentListView(generics.ListAPIView):
    serializer_class = serializers.CreateIncidentReportSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = IncidentReport.objects.all()
        location = self.request.query_params.get('location')
        reported_date = self.request.query_params.get('reported_at')
        incident_type = self.request.query_params.get('incident_type')
        status = self.request.query_params.get('is_status_open')
        if status == 'true':
            queryset = queryset.filter(is_status_open=True)
        elif status == 'false':
            queryset = queryset.filter(is_status_open=False)
        elif location:
            queryset = queryset.filter(location__name=location)
        elif reported_date:
            queryset = queryset.filter(reported_at=reported_date)
        elif incident_type:
            queryset = queryset.filter(incident_type__label=incident_type)
        return queryset.order_by('-reported_at')
    
