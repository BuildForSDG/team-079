"""Views for responder."""
from rest_framework import viewsets, generics

from .models import Responder
from .serializers import ResponderSerializer


class ResponderViewset(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer


class LocationView(generics.ListAPIView):
    from reporter.models import IncidentLocation
    from reporter.serializers import IncidentLocationSerializer
    queryset = IncidentLocation.objects.all()
    serializer_class = IncidentLocationSerializer


def process_incident_type(incident_type):
    place_type = ''
    if incident_type == 'Arm Robbery':
        place_type = 'police'
    elif incident_type in ['Pedestrian Knock Down', 'Hit and Run', 'Motor Vehicle Collision', 'Uncategorized']:
        place_type = 'hospital'
    return place_type


def find_responder(request):
    from reporter.models import IncidentReport
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse
    import requests
    import json

    incident_id = request.GET.get('incident')

    incident = get_object_or_404(IncidentReport, pk=incident_id)
    latitude = incident.location.latitude
    longitude = incident.location.longitude
    location = f'{str(latitude)},{str(longitude)}'
    place_type = process_incident_type(incident.incident_type.label)

    # construct the query parameters
    payload = {
        'location': location,
        'radius': 500,
        'types': place_type,
        'key': 'AIzaSyBr427Ow25KCsgHcHQe_J1V1L39nTouIfk'
    }
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    response = requests.get(url, params=payload)

    # get the first five places
    MAX_OBJECT = 5
    rsp = json.loads(response.text)['results'][:MAX_OBJECT]

    return JsonResponse(rsp, safe=False)
