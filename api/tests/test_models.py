from django.test import TestCase
from mimesis import Generic

from authapi.models import User
from api.models import Profile


class ProfileTestCase(TestCase):
    def setUp(self):
        self.gen = Generic()
        self.new_user = User(
            first_name=self.gen.person.full_name().split()[0],
            last_name=self.gen.person.full_name().split()[1],
            email=self.gen.person.email(),
            raw_password=self.gen.person.password()
        )
        self.new_user.save()

    def test_profile_instance(self):
        self.user_profile = Profile(user=self.new_user)

        self.assertIsInstance(self.user_profile, Profile)

    def test_profile_save(self):
        self.user_profile = Profile(
            user=self.new_user,
            height=int(float(self.gen.person.height())*100),
            weight=self.gen.person.weight(),
            country="Kerbal",
            city="Kerbal"
            )
        self.user_profile.save_profile()
        self.all_profiles = Profile.objects.all()

        self.assertIn(self.user_profile, self.all_profiles)