from django.test import SimpleTestCase
from django.urls import reverse, resolve
from USERS.views import (register, ProfileDetailView)


class TestUrls(SimpleTestCase):

    # Reverse the register url
    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    # Reverse the profile url
    def test_profile_url(self):
        url = reverse('profile', args=['1'])
        self.assertEquals(resolve(url).func.view_class, ProfileDetailView)
