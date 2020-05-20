"""Views for responder."""
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import json, requests
from django.shortcuts import get_object_or_404
from django.core import serializers
from .models import Responder
from .serializers import ResponderSerializer
from reporter.models import IncidentReport, IncidentLocation
from reporter.serializers import IncidentLocationSerializer


class ResponderViewset(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer


class LocationView(generics.ListAPIView):
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
    incident_id = request.GET.get('incident')

    incident = get_object_or_404(IncidentReport, pk=incident_id)
    latitude = incident.location.location_lat
    longitude = incident.location.location_lng
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


@api_view(['POST', 'PUT'])
def assign_responder(request, pk):
    # this function accepts a request of a responder's location, add an entry in the location table
    # creates a responder to this incident and object the incident with the responder

    # pass json payload
    data = json.loads(request.body)
    name = data['map_name']
    location = IncidentLocation.objects.create(**data)

    # construct responder data
    responder_data = {
        'name': name,
        'location': location
    }
    responder = Responder.objects.create(**responder_data)

    # update incident
    incident = get_object_or_404(IncidentReport, pk=pk)
    incident.responder = responder
    incident.is_status_open = False
    incident.save()

    response = {'message': "HELp is On the Way!"}
    return JsonResponse(response)
