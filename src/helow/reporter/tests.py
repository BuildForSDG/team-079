"""Test module for all reporter app entities."""
from django.test import TestCase
from reporter.models import IncidentReport, IncidentLocation, IncidentType
from datetime import datetime
from django.contrib.auth.models import User


# Create your tests here.
class UrlTest(TestCase):
    """Test class for reporter urls."""

    def test_report_incident_successful(self):
        """Returns 200 if path is valid."""
        create_report = self.client.get('/api/v1/incident/report/')
        self.assertEquals(create_report.status_code, 200)


class IncidentReportTest(TestCase):
    """Tests if a new incident report is created successfully."""

    @classmethod
    def setUpTestData(cls):
        """Setup sample data for class use."""
        # create an incident type
        incident_type = IncidentType(label='Type1', frequency=0)
        incident_type.save()

        # create an incident location
        incident_location = IncidentLocation(name='Aguda', latitude=43.9, longitude=-45.2)
        incident_location.save()

        # create user
        # create a new user
        user = User(username='techie', email='techie@gmail.com', password='Password12')
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
        incident_location = IncidentLocation.objects.get(id=1)
        self.assertEquals(incident_location.name, 'Aguda')

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
        location = IncidentLocation.objects.get(id=1)
        self.assertEquals(incident.location, location)
