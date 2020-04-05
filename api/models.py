import uuid

from django.db import models
from authapi.models import User
from itertools import groupby


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


class Chat(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sender_user'
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='receiver_user'
    )
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def save_chat(self):
        self.save()

    @classmethod
    def get_conversations(cls, user):
        recipients = []
        all_chats = cls.objects.filter(sender=user).all()

        for chat in all_chats:
            obj = {}
            obj['public_id'] = chat.receiver.public_id
            obj['first_name'] = chat.receiver.first_name
            obj['last_name'] = chat.receiver.last_name

            recipients.append(obj)

        return list(map(dict, set(tuple(sorted(d.items())) for d in recipients)))

    @classmethod
    def get_conversation(cls, recipient, sender):
        conversation_chats = Chat.objects.filter(receiver=recipient, sender=sender).all()

        return conversation_chats


class Symptom(models.Model):
    name = models.CharField(max_length=64)

    @classmethod
    def create_symptoms(cls, data, key="name"):
        pat_symptoms = []
        for item in data:
            string_name = item[key]
            db_symptom = cls.objects.filter(name=string_name.lower().capitalize()).first()

            if db_symptom is None:
                new_symptom = cls(name=string_name.lower().capitalize())
                new_symptom.save()
                pat_symptoms.append(new_symptom)

            else:
                pat_symptoms.append(db_symptom)

        return set(pat_symptoms)


class Examination(models.Model):
    posted_at = models.DateTimeField(auto_now_add=True)
    examination_date = models.DateTimeField(blank=True, null=True)
    prescription_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=5)
    patient_note = models.TextField()
    doctor_note = models.TextField(blank=True, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='patient',on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='doctor',on_delete=models.CASCADE)
    symptoms = models.ManyToManyField(Symptom)

    def save_exam(self):
        self.save()