"""Module that exposes all the backed APIs of the HELOW."""
from django.urls import path
from rest_framework.routers import DefaultRouter
from reporter import views

router = DefaultRouter()
router.register('incident/types', views.IncidentTypesViewset, basename='incident_types')
router.register('users', views.UserViewset, basename='users')


urlpatterns = [
    path('incident/report/', views.CreateIncidentReportView.as_view(), name='report_incident'),
    path('incident/report/<int:pk>', views.DetailIncidentReportView.as_view(), name='incident_detail'),
    path('incident/report/filter', views.IncidentListView.as_view(), name="incident_filter"),
]
urlpatterns += router.urls
