from django.test import TestCase, Client
from django.utils import timezone
from ..views import *
from ..models import *


class TestViews(TestCase):
    """
    Tests the Meetings module views
    """

    def setUp(self):
        self.client = Client()

        # Create user for login
        self.user = User.objects.create_user('Andres', 'mxb774@case.edu', 'Demo1234')
        self.user2 = User.objects.create_user('Thomas', 'thomaspatton@case.edu', 'Demo1234')
        self.client.login(username='Andres', password='Demo1234')

        # Create a meeting and add User to the meeting
        self.meeting = Meeting.objects.create(
            title='Demo',
            university='CWRU',
            course='EECS 393',
            date_start=timezone.now(),
            date_end=timezone.now(),
            location='Olin',
            description='Demo'
        )

        # Add member
        self.mem1 = Membership.objects.create(
            person=self.user,
            group=self.meeting,
            date_joined=timezone.now(),
            is_organizer=True
        )

        self.create_url = reverse('meeting-create')
        self.list_url = reverse('meetings-list')
        self.search_url = reverse('meeting-search')
        self.detail_url = reverse('meeting-detail', args=[self.meeting.pk])
        self.update_url = reverse('meeting-update', args=[self.meeting.pk])
        self.delete_url = reverse('meeting-delete', args=[self.meeting.pk])

    def test_meeting_create_GET(self):
        response = self.client.get(self.create_url)
        self.assertEquals(response.status_code, 200)

    def test_meeting_list_GET(self):
        response = self.client.get(self.list_url)
        self.assertEquals(response.status_code, 200)

    def test_meeting_search_GET(self):
        response = self.client.get(self.search_url)
        self.assertEquals(response.status_code, 200)

    def test_meeting_detail_GET(self):
        response = self.client.get(self.detail_url)
        self.assertEquals(response.status_code, 200)

    def test_meeting_update_GET(self):
        response = self.client.get(self.update_url)
        self.assertEquals(response.status_code, 200)

    def test_meeting_delete_GET(self):
        response = self.client.get(self.delete_url)
        self.assertEquals(response.status_code, 200)

    def test_create_membership_function(self):
        create_membership(self.user2, self.meeting, False)
        query_count = Membership.objects.filter(group=self.meeting, person=self.user2).count()
        self.assertEqual(query_count, 1)

    def test_join_and_leave_meeting_POST(self):
        # Join Meeting
        self.client.logout()
        new_user = User.objects.create_user('David', 'david@case.edu', 'Demo1234')
        self.client.login(username='David', password='Demo1234')
        self.client.post(self.detail_url, {'join_meeting': 'Join Meeting'}, follow=True)
        query_count = new_user.user_meetings.all().count()
        self.assertEqual(query_count, 1)

        # Leave meeting
        self.client.post(self.detail_url, {'leave_meeting_mem': 'Leave Meeting'}, follow=True)
        query_count = new_user.user_meetings.all().count()
        self.assertEqual(query_count, 0)

    def test_leave_meeting_organizer_only_member_POST(self):
        self.client.post(self.detail_url, {'leave_form': 'Leave meeting', 'name': 'leave_form'},
                         content_type='application/json', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        query_count = self.user.user_meetings.all().count()
        # user is the only member, so he/she cannot leave
        self.assertEqual(query_count, 1)

    def test_leave_meeting_organizer_choose_member_POST(self):
        create_membership(self.user2, self.meeting, False)
        self.client.post(self.detail_url, {'leave_form': 'Leave meeting', 'name': 'leave_form'},
                         content_type='application/json', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.client.post(self.detail_url,
                         {'leave_meeting_org': 'Assign and leave meeting',
                          'select_org': self.user2})

        # organizer left, so no meetings for him/her
        query_count = self.user.user_meetings.all().count()
        self.assertEqual(query_count, 0)

        # user2 is the new organizer
        membership = Membership.objects.get(group=self.meeting, person=self.user2)
        self.assertTrue(membership.is_organizer)
