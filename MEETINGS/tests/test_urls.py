from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (MeetingListView, MeetingDetailView, MeetingCreateView, MeetingUpdateView, MeetingDeleteView,
                     SearchListView)


class TestUrls(SimpleTestCase):
    """
    These test cases check the urls of the Meetings module
    """

    def test_meeting_list_url(self):
        url = reverse('meetings-list')
        self.assertEquals(resolve(url).func.view_class, MeetingListView)

    def test_meeting_create_url(self):
        url = reverse('meeting-create')
        self.assertEquals(resolve(url).func.view_class, MeetingCreateView)

    def test_meeting_detail_url(self):
        url = reverse('meeting-detail', args=['1'])
        self.assertEquals(resolve(url).func.view_class, MeetingDetailView)

    def test_meeting_update_url(self):
        url = reverse('meeting-update', args=['1'])
        self.assertEquals(resolve(url).func.view_class, MeetingUpdateView)

    def test_meeting_delete_url(self):
        url = reverse('meeting-delete', args=['1'])
        self.assertEquals(resolve(url).func.view_class, MeetingDeleteView)

    def test_meeting_search_url(self):
        url = reverse('meeting-search')
        self.assertEquals(resolve(url).func.view_class, SearchListView)

