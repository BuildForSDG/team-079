from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    msg = """
    Welcome to HELOW API Backend! HElp is On the Way! Kindly access the API documentation using any of the following
    for more information:\n
    http://127.0.0.1:8000/api/v1/swagger/,\n
    http://127.0.0.1:8000/api/v1/redoc/,
    http://127.0.0.1:8000/docs/
    """
    return HttpResponse(msg)
