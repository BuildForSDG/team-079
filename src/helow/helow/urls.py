"""
HELOW URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
https://docs.djangoproject.com/en/3.0/topics/http/urls/

Examples are

Function views
--------------
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
-----------------
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
-------------------------
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view as drf
from drf_yasg import openapi
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from webapp.views import home

# for building documentation
TITLE = "HELOW API"
DESCRIPTION = "Accidents on the highways are inevitable. However, it should not be a death sentence. " \
              "We want to mitigate the mortality rates by developing a smart report/response system on the go." \
              "HElp is On the Way!"

drf_schema_view = drf(
    openapi.Info(
        title=TITLE,
        default_version='v1',
        description=DESCRIPTION,
        terms_of_service="https://www.meety.com/policies/terms/",
        contact=openapi.Contact(email="techiefrankie@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

schema_view = get_schema_view(title=TITLE)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),

    # user registration/authentication
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/',
         include('rest_auth.registration.urls')),

    # api documentation
    path('api/v1/swagger-json', drf_schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/swagger/', drf_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', drf_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('docs/', include_docs_urls(title=TITLE, description=DESCRIPTION)),
]
