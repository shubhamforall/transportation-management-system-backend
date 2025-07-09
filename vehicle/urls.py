from django.urls import path, include

urlpatterns = [path("", include("vehicle.routes.vehicle"))]
