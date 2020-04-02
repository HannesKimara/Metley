from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import (
    IsAuthenticated, IsAuthenticatedOrReadOnly
)

from ..models import Clinic
from ..serializers import ClinicSerializer


class ClinicView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_clinics = Clinic.objects.all()
        serializer = ClinicSerializer(all_clinics, many=True)

        return Response(
            {
                'total': len(all_clinics),
                'results': serializer.data,
            }
        )