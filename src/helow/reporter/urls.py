"""Module that exposes all the backed APIs of the HELOW."""
from django.urls import path
from rest_framework.routers import SimpleRouter
from reporter import views

router = SimpleRouter()
router.register('incident/types', views.IncidentTypesViewset, basename='incident_types')

urlpatterns = [
    path('incident/report/', views.CreateIncidentReportView.as_view(), name='report_incident'),
    path('incident/report/<int:pk>', views.DetailIncidentReportView.as_view(), name='incident_detail'),
]
urlpatterns += router.urls
