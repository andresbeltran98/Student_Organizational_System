from django.test import TestCase
from ..models import Meeting, Membership
from django.contrib.auth.models import User
import datetime


class MeetingTestModel(TestCase):

    def setUp(self):
        self.title = 'MyMeeting'
        self.course = 'EECS 383'
        self.date_now = datetime.datetime.strptime('2019-3-19', "%Y-%m-%d").date()
        self.location = 'Sears'
        self.description = 'Demo Session'

        self.meeting1 = Meeting.objects.create(
            title=self.title,
            course=self.course,
            date=self.date_now,
            location=self.location,
            description=self.description
        )

        # Add member
        self.username = 'Andres'
        self.person = User.objects.create_user(username=self.username)
        self.group = self.meeting1
        self.date_joined = datetime.datetime.now()
        self.is_organizer = True

        self.mem1 = Membership.objects.create(
            person=self.person,
            group=self.group,
            date_joined=self.date_joined,
            is_organizer=self.is_organizer
        )

    def test_get_parameters(self):
        self.assertEquals(self.meeting1.title, self.title)
        self.assertEquals(self.meeting1.course, self.course)
        self.assertEquals(self.meeting1.date, self.date_now)
        self.assertEquals(self.meeting1.location, self.location)
        self.assertEquals(self.meeting1.description, self.description)

    def test_meeting_members(self):
        self.assertEquals(self.meeting1.members.get(username=self.username), self.person)

    def test_user_meetings(self):
        self.assertEquals(self.person.user_meetings.get(title=self.title), self.meeting1)

