from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.permissions import (
    IsAuthenticated
)

from ..models import Profile
from ..serializers import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile = Profile.objects.filter(user=request.user).first()
        serializer = ProfileSerializer(user_profile)
        
        return Response(
            {
                'user': {
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'email': request.user.email,
                    'date_joined': request.user.date_joined,
                    'last_login': request.user.last_login,
                    'profile': serializer.data
                }
            }
        )

    def post(self, request):
        serializer = ProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )