"""Test calss for responders."""
from datetime import datetime

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient

from reporter.tests import generate_password
from responder.models import Responder
from reporter.models import Place, IncidentReport, IncidentType


class ResponderTest(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # create a place
        self.place = Place.objects.create(map_name='Aguda', location_lat=43.9, location_lng=-45.2)

        # create incident type
        self.incident_type = IncidentType.objects.create(label='Collision', frequency=0)

        # create a new user
        self.user = User.objects.create(username='techie', email='techie@gmail.com', password=generate_password())

        # create an incident
        self.incident_report = IncidentReport.objects.create(title="title1", description='long detail',
                                                             incident_type=self.incident_type, location=self.place,
                                                             reported_at=datetime.now(), reported_by=self.user)

        # create a responder
        self.responder = Responder.objects.create(name='Aguda Orthopaedic Hospital', location=self.place)

    def test_responders_list(self):
        """Returns status code 200 if get find nearby responders list url is functional."""
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/responder/find/?incident={self.incident_report.id}')
        self.assertEquals(response.status_code, 200, f"Expected response code 200, got {response.status_code}")

    def test_place_list(self):
        """Returns status code 200 if the url to assign a responder to an incident returns successful."""
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/responder/assign/{self.incident_report.id}?place_id'
                                   f'=ChIJYcHoGyRawokR9rSZ9FTdFMk')
        self.assertEquals(response.status_code, 200, f"Expected response code 200, got {response.status_code}")
