from django.test import SimpleTestCase
from django.urls import reverse, resolve
from USERS.views import (register, profile)


class TestUrls(SimpleTestCase):

    def test_register_url(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func, register)

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEquals(resolve(url).func, profile)
