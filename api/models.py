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