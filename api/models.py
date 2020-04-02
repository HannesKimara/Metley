import uuid

from django.db import models
from authapi.models import User


class Profile(models.Model):
    birth_date = models.DateField(blank=True, null=True)
    height = models.IntegerField()
    weight = models.FloatField()
    country = models.CharField(max_length=32)
    city = models.CharField(max_length=48)
    is_doctor = models.BooleanField(default=False)
    bio = models.TextField(default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def save_profile(self):
        self.save()


class Clinic(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=32)
    field_practice = models.CharField(max_length=32)
    description = models.TextField()
    phone_number = models.CharField(max_length=16)
    email = models.EmailField(unique=True)
    country = models.CharField(max_length=32)
    city = models.CharField(max_length=48)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def save_clinic(self):
        self.save()

    @classmethod
    def search_clinic_id(cls, pub_id):
        return cls.objects.filter(public_id=pub_id).first()

    @classmethod
    def search_field(cls, field):
        return cls.objects.filter(public_id__icontains=field).all()