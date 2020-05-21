"""Views for responder."""
from rest_framework import viewsets, generics
from django.http import JsonResponse
import json, requests
from django.shortcuts import get_object_or_404
from .models import Responder
from .serializers import ResponderSerializer
from reporter.models import IncidentReport, Place
from reporter.serializers import IncidentLocationSerializer
from setup import logger
from config import Config


class ResponderViewset(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer


class LocationView(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = IncidentLocationSerializer


def process_incident_type(incident_type):
    """A function stub to get the place type by the incident type."""
    place_type = ''
    if incident_type == 'Arm Robbery':
        place_type = 'police'
    elif incident_type in ['Pedestrian Knock Down', 'Hit and Run', 'Motor Vehicle Collision', 'Uncategorized']:
        place_type = 'hospital'
    logger.info(f'Returning place type: {place_type} for incident of type: {incident_type}')

    return place_type


def get_incident_data(incident_id):
    """A function to return incident location and type given an id."""
    logger.info(f'Looking up responders for incident with id: {incident_id}')

    try:
        incident = IncidentReport.objects.get(id=incident_id)
    except ValueError:
        logger.error(f'An integer variable expect but got {incident_id}')
        return None, None

    location, place_type = None, None

    if incident:
        try:
            latitude = incident.location.location_lat
            longitude = incident.location.location_lng
            location = f'{str(latitude)},{str(longitude)}'
            place_type = process_incident_type(incident.incident_type.label)
        except AttributeError:
            logger.error(f'{incident} with id {incident_id} does not have attributes for all fields')
            return None, None

    return location, place_type


def find_responders(request):
    """This function used the latitude and longitude of an incident location to search for nearby responders."""
    incident_id = request.GET.get('incident')
    location, place_type = get_incident_data(incident_id)

    rsp = []
    if location is not None and place_type is not None:
        # construct the query parameters
        payload = {
            'location': location,
            'radius': 500,
            'types': place_type,
            'key': Config.MAP_API_KEY
        }

        url = Config.MAP_NEARBY_SEARCH
        logger.info(f"Call {url} with parameters: {payload}")

        try:
            response = requests.get(url, params=payload)

            rsp = json.loads(response.text)
            if 'results' in rsp and len(rsp.get('results')) > 0:
                # get the first MAX_PLACES results
                rsp = rsp['results'][:Config.MAX_PLACES]
        except Exception as ex:
            logger.error(f"Exception caught: {ex.__class__.__name__} exception: {ex}")
    else:
        rsp = {"message": f"Bad input received. Please validate that {incident_id} is accurate"}

    return JsonResponse(rsp, safe=False)


def assign_responder(request, pk):
    """this function accepts a request of a responder's location, add an entry in the location table
    creates a responder to this incident and object the incident with the responder."""

    # pass json payload
    place_id = request.GET.get('place_id')

    place_data = get_location_data(place_id)  # get the responder data

    if len(place_data) > 0:
        location = Place.objects.create(**place_data)  # add location entry for this responder

        # construct responder data
        name = place_data['map_name']
        responder_data = {
            'name': name,
            'location': location
        }
        responder = Responder.objects.create(**responder_data)  # create a responder

        # update incident
        update_incident(pk, responder)

        response = {
            "message": "HELp is On the Way",
            "formatted_address": place_data["formatted_address"],
            "formatted_phone_number": place_data["formatted_phone_number"],
            "international_phone_number": place_data["international_phone_number"],
            "url": place_data["url"],
            "website": place_data["website"]
        }
    else:
        response = {"message": f"No place found for the id: {place_id}"}

    return JsonResponse(response)


def update_incident(pk, responder):
    # update incident
    incident = get_object_or_404(IncidentReport, pk=pk)
    incident.responder = responder
    incident.is_status_open = False
    incident.save()


def get_location_data(place_id):
    """Function to load a place data with its place_id."""
    location = {}

    # construct the query parameters
    payload = {
        'placeid': place_id,
        'key': Config.MAP_API_KEY
    }

    url = Config.MAP_PLACE_DETAIL
    logger.info(f'Call to {url} with parameters: {payload}')

    try:
        rsp = requests.get(url, params=payload)
        # parse response from endpoint
        response = json.loads(rsp.text)
        logger.debug(f'Raw response: {response}')

        if 'result' in response and len(response.get('result')) is not 0:
            # parse only the result object

            response = response['result']
            logger.info(f'Parse response: {response}')

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
        logger.debug(f'No data found for place with id: {place_id}')
    except Exception as ex:
        logger.error(f"Exception caught: {ex.__class__.__name__}, message: {ex}")

    return location
