from rest_framework import serializers

from .models import Profile, Clinic
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


class ClinicSerializer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=2)
    field_practice = serializers.CharField(max_length=32)
    description = serializers.CharField(min_length=8)
    phone_number = serializers.CharField(min_length=8, max_length=16)
    email = serializers.EmailField()
    country = serializers.CharField(min_length=2, max_length=32)
    city = serializers.CharField(min_length=2, max_length=48)
    
    class Meta:
        model = Clinic
        exclude = ['public_id', 'owner']