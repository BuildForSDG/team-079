from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ResponderViewset, ResponderFilteredView

router = DefaultRouter()
router.register('responder', ResponderViewset, basename='responder')

urlpatterns = [
    path('responder/find/', ResponderFilteredView.as_view(), name='find_responder'),
]

urlpatterns += router.urls
