"""Module that exposes all the backed APIs of the HELOW."""
from django.urls import path
from reporter import views

urlpatterns = [
    path('incident/report/', views.CreateIncidentReportView.as_view(), name='report_incident'),
    path('incident/report/<int:pk>', views.DetailIncidentReportView.as_view())
]
