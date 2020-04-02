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

    def post(self, request):
        serializer = ClinicSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(
                owner=request.user
            )
            return Response(
                {
                    'data':serializer.data,
                    'message':'Your clinic is awaiting approval, an email will be sent with more info',
                },
                status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )