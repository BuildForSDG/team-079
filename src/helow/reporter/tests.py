"""Test module for all reporter app entities."""
from django.test import TestCase
from reporter.models import IncidentReport, Place, IncidentType
from datetime import datetime
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from rest_framework.test import APIClient, APITestCase


def generate_password():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&amp;*(-_=+)'
    return get_random_string(12, chars)


# Create your tests here.
class UrlTest(TestCase):
    """Test class for reporter urls."""

    def test_report_incident_successful(self):
        """Returns 200 if path is valid."""
        create_report = self.client.get('/api/v1/incident/report/')
        self.assertEquals(create_report.status_code, 200)


class IncidentReportTest(TestCase):
    """Tests class for incident report."""

    @classmethod
    def setUpTestData(cls):
        """Setup sample data for class use."""
        # create an incident type
        incident_type = IncidentType(label='Type1', frequency=0)
        incident_type.save()

        # create an incident location
        incident_location = Place(map_name='Aguda', location_lat=43.9, location_lng=-45.2)
        incident_location.save()

        # create user
        # create a new user
        user = User(username='techie', email='techie@gmail.com', password=generate_password())
        user.save()

        # create an incident
        incident_report = IncidentReport(title="title1", description='long detail',
                                         incident_type=incident_type, location=incident_location,
                                         reported_at=datetime.now(),
                                         reported_by=user)
        incident_report.save()

    # create assertions
    def test_incident_type_created(self):
        """Returns true if incident type created successfully."""
        incident_type = IncidentType.objects.get(id=1)
        self.assertEquals(incident_type.label, 'Type1')

    def test_incident_location_created(self):
        """Returns true if incident location created successfully."""
        incident_location = Place.objects.get(id=1)
        self.assertEquals(incident_location.map_name, 'Aguda')

    def test_user_created(self):
        """Returns true if user created successfully."""
        user = User.objects.get(id=1)
        self.assertEquals(user.username, 'techie')

    def test_incident_report_created(self):
        """Returns true if incident report created successfully."""
        report = IncidentReport.objects.get(id=1)
        self.assertEquals(report.title, 'title1')

    def test_incident_location_valid(self):
        """Returns true if incident has a valid location."""
        incident = IncidentReport.objects.get(id=1)
        location = Place.objects.get(id=1)
        self.assertEquals(incident.location, location)

    def test_incident_type_frequency_incremented(self):
        """Returns true if the frequency of this incident's type was incremented."""
        incident_type = IncidentType.objects.get(id=1)
        self.assertEquals(incident_type.frequency, 1)


class IncidentTypesTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # create an incident type to be used for testing
        self.incident_type = IncidentType.objects.create(id=1, label='test', frequency=0)

    def test_incident_types_list(self):
        """Returns status code 200 if get incident type list url is functional."""
        response = self.client.get('http://127.0.0.1:8000/api/v1/incident/types/')
        self.assertEquals(response.status_code, 200, f"Expected response code 200, got {response.status_code}")

    def test_incident_type_detail(self):
        """Returns status code 200 if get incident type detail url is functional."""
        response = self.client.get(f'http://127.0.0.1:8000/api/v1/incident/types/{self.incident_type.id}/')
        self.assertEquals(response.status_code, 200, f"Expected response code 200, got {response.status_code}")


# testing the filter endpoints.
class IncidentReportFilterTest(TestCase):
    """Test class for filter and pagination urls."""

    def test_report_incident_filter_successful(self):
        """Returns 200 if path is valid."""
        create_report = self.client.get('/api/v1/incident/report/filter')
        self.assertEquals(create_report.status_code, 200)