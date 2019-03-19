from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_url = reverse('meeting-create')

    def test_meeting_list_GET(self):
        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 302)
        self.assertTemplateUsed(response, 'meeting_form.html')