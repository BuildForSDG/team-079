"""View classes for reporter app."""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from reporter.models import IncidentReport, IncidentType
from reporter import serializers
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth import get_user_model
from config import Config as config
from setup import logger


# Create your views here.
class CreateIncidentReportView(generics.ListCreateAPIView):
    serializer_class = serializers.CreateIncidentReportSerializer

    # return incidents in descending order
    def get_queryset(self):
        queryset = IncidentReport.objects.all()
        queryset = queryset.filter(status=config.INCIDENT_STATUS.get("STATUS_PENDING"))
        return queryset.order_by('-id')


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
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=config.INCIDENT_STATUS.get(status))
        elif location:
            queryset = queryset.filter(location__name=location)
        elif reported_date:
            queryset = queryset.filter(reported_at=reported_date)
        elif incident_type:
            queryset = queryset.filter(incident_type__label=incident_type)
        return queryset.order_by('-reported_at')


class IncidentTypesViewset(viewsets.ModelViewSet):
    queryset = IncidentType.objects.all()
    serializer_class = serializers.IncidentTypeSerializer


class UserViewset(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer

@csrf_exempt
def report_incident(request):
    """Function to create new incident."""
    import json
    from reporter.models import Place

    try:
        # parse the request body
        body = json.loads(request.body)

        # get user
        if not request.user.is_anonymous:
            body['reported_by'] = request.user

        # get incident type
        body['incident_type'] = IncidentType.objects.get(id=body.get('incident_type'))

        # get location
        location = Place.objects.create(owner=config.REPORTER_LOCATION, **body.pop('location'))

        # create incident
        incident = IncidentReport.objects.create(location=location, **body)

        # call find_responders to scan for available responders
        from django.shortcuts import redirect, reverse

        return redirect(reverse('find_responder') + f'?incident={incident.id}')
    except (TypeError, ValueError):
        logger.error(f"Error occurred while processing request {request}.")
        return JsonResponse({"message": "Error occurred, please kindly validate input data"})
