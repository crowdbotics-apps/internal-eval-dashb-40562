from django.urls import path, include
from rest_framework.routers import DefaultRouter

from googlesheets.api.v1.viewsets import SheetsView


urlpatterns = [
    path("", SheetsView.as_view(), name="sheets-view")
]
