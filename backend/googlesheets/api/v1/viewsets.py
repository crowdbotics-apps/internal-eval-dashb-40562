from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from googlesheets.repository import GoogleSheetsRepository


class SheetsView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            results = GoogleSheetsRepository.execute()
            return Response(results)
        except Exception as err:
            raise ValidationError(f"Error fetching sheets data: {err}")
