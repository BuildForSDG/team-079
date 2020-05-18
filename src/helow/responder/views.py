"""Views for responder."""
from rest_framework import viewsets, generics
from .models import Responder
from .serializers import ResponderSerializer


class ResponderViewset(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer


class ResponderFilteredView(generics.ListAPIView):
    serializer_class = ResponderSerializer

    def get_queryset(self):
        queryset = Responder.objects.all()
        incident_id = self.request.query_params.get('incident', None)

        from reporter.models import IncidentReport
        from django.shortcuts import get_object_or_404

        incident = get_object_or_404(IncidentReport, pk=incident_id)
        latitude = incident.location.latitude
        longitude = incident.location.longitude
        print(longitude, latitude)


        return queryset.order_by('id')
