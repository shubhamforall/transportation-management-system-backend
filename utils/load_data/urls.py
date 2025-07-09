from django.urls import path
from utils.load_data import views
from utils.functions import is_local

urlpatterns = []

if is_local():
    urlpatterns.append(path('load-pre-data', views.LoadPreDataView.as_view(), name="load_pre_data"))