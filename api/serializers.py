from rest_framework import serializers

from .models import Profile
from authapi.models import User


class ProfileSerializer(serializers.ModelSerializer):
    birth_date = serializers.DateField(required=False)
    height = serializers.IntegerField()
    weight = serializers.FloatField()
    country = serializers.CharField(min_length=2)
    city = serializers.CharField(min_length=2)
    is_doctor = serializers.BooleanField(default=False)
    bio = serializers.CharField(default="")

    class Meta:
        model = Profile
        exclude = ['id', 'user']