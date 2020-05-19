from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ResponderViewset, LocationView, find_responder

router = DefaultRouter()
router.register('responder', ResponderViewset, basename='responder')

urlpatterns = [
    path('responder/find/', find_responder, name='find_responder'),
    path('incident/location/', LocationView.as_view(), name='incident_location'),
]

urlpatterns += router.urls
