"""Views for responder."""
from rest_framework import viewsets, generics
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
import json, requests
from django.shortcuts import get_object_or_404
from django.core import serializers
from .models import Responder
from .serializers import ResponderSerializer
from reporter.models import IncidentReport, Place
from reporter.serializers import IncidentLocationSerializer


class ResponderViewset(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer


class LocationView(generics.ListAPIView):
    queryset = Place.objects.all()
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


@api_view(['GET', 'POST', 'PUT'])
def assign_responder(request, pk):
    # this function accepts a request of a responder's location, add an entry in the location table
    # creates a responder to this incident and object the incident with the responder

    # pass json payload
    place_id = request.GET.get('place_id')

    place_data = get_location_data(place_id)

    location = Place.objects.create(**place_data)

    # construct responder data
    name = place_data['map_name']
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

    response = {
        "message": "HELp is On the Way",
        "formatted_address": place_data["formatted_address"],
        "formatted_phone_number": place_data["formatted_phone_number"],
        "international_phone_number": place_data["international_phone_number"],
        "url": place_data["url"],
        "website": place_data["website"]
    }
    return JsonResponse(response)


def get_location_data(place_id):
    location = {}

    # construct the query parameters
    payload = {
        'place_id': place_id,
        'key': 'AIzaSyBr427Ow25KCsgHcHQe_J1V1L39nTouIfk'
    }
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    rsp = requests.get(url, params=payload)

    # parse response from endpoint
    response = json.loads(rsp.text)['result']
    location['map_name'] = response['name']
    location['location_lat'] = response['geometry']['location']['lat']
    location['location_lng'] = response['geometry']['location']['lng']
    location['viewport_ne_lat'] = response['geometry']['viewport']['northeast']['lat']
    location['viewport_ne_lng'] = response['geometry']['viewport']['northeast']['lng']
    location['viewport_sw_lat'] = response['geometry']['viewport']['southwest']['lat']
    location['viewport_sw_lng'] = response['geometry']['viewport']['southwest']['lng']
    location['formatted_address'] = response['formatted_address']
    location['formatted_phone_number'] = response['formatted_phone_number']
    location['international_phone_number'] = response['international_phone_number']
    location['place_id'] = response['place_id']
    location['rating'] = response['rating']
    location['vicinity'] = response['vicinity']
    location['url'] = response['url']
    location['website'] = response['website']

    return location
