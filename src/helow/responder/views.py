"""Views for responder."""
from rest_framework import viewsets
from .models import Responder
from .serializers import ResponderSerializer


class ResponderViewset(viewsets.ModelViewSet):
    queryset = Responder.objects.all()
    serializer_class = ResponderSerializer
