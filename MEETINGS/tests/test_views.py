from django.test import TestCase, Client
from django.urls import reverse


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.create_url = reverse('meeting-create')
        self.list_url = reverse('meetings-list')
        self.search_url = reverse('meeting-search')
        self.detail_url = reverse('meeting-detail', args=['1'])
        self.update_url = reverse('meeting-update', args=['1'])
        self.delete_url = reverse('meeting-delete', args=['1'])

    def test_meeting_create_GET(self):
        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 302)

    def test_meeting_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 302)

    def test_meeting_search_GET(self):
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 302)

    def test_meeting_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 302)

    def test_meeting_update_GET(self):
        response = self.client.get(self.update_url)
        self.assertEquals(response.status_code, 302)

    def test_meeting_delete_GET(self):
        response = self.client.get(self.delete_url)
        self.assertEquals(response.status_code, 302)