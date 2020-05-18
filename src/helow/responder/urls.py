from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ResponderViewset

router = DefaultRouter()
router.register('responder', ResponderViewset, basename='responder')

urlpatterns = router.urls

urlpatterns += [

]
