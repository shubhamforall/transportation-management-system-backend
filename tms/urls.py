"""
URL configuration for tms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from .swagger import get_token_auth_schema

get_token_auth_schema()

urlpatterns = [
    # User Management API
    path("api/", include("auth_user.urls")),
    
    # Customer Management API
    path("api/", include("customer.urls")),
    
    #Vehicle Management API
    path("api/", include("vehicle.urls")),
    
    #Invoice Management API
    path("api/", include("invoice.urls")),

    # Payment Management API
    path("api/", include("payment.urls")),
    
    # User load data API
    path("api/", include("utils.load_data.urls")),
    
    # Swagger Documentation
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
