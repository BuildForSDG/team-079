"""Manage views functions for webapp."""
from django.http import HttpResponse


# Create your views here.
def home(request):
    """View function for home route."""
    msg = """
    HELOW API DOCS
    
    Welcome to HELOW API Backend! HElp is On the Way! Kindly access the API documentation using any of the following
    for more information:
    http://127.0.0.1:8000/api/v1/swagger/,
    http://127.0.0.1:8000/api/v1/redoc/,
    http://127.0.0.1:8000/docs/
    """
    return HttpResponse(msg)
