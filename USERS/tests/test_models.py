from django.test import TestCase
from ..models import Profile
from django.contrib.auth.models import User
import datetime


class ProfileTestModel(TestCase):

    # Create a sample user
    def setUp(self):
        self.username = 'TestUser'
        self.user = User.objects.create_user(username=self.username, first_name="Thomas", last_name="Patton",
                                                email="tjpatton1@gmail.com")
        self.user.profile.university = "CWRU"
        self.user.profile.major = "Computer Science"

    # Test if the user's values are correctly passed through
    def test_get_parameters(self):
        self.assertEquals(self.user.first_name, "Thomas")
        self.assertEquals(self.user.last_name, "Patton")
        self.assertEquals(self.user.username, "TestUser")
        self.assertEquals(self.user.email, "tjpatton1@gmail.com")
        self.assertEquals(self.user.profile.major, "Computer Science")
        self.assertEquals(self.user.profile.university, "CWRU")
