from django.test import TestCase
from ..models import Meeting, Membership
from django.contrib.auth.models import User
import datetime
from django.utils import timezone


class MeetingTestModel(TestCase):
    """
    These test cases check the creation of new Meeting and Membership instances
    """

    def setUp(self):
        self.title = 'MyMeeting'
        self.university = 'CWRU'
        self.course = 'EECS 383'
        self.date_now = timezone.now()
        self.location = 'Sears'
        self.description = 'Demo Session'

        self.meeting1 = Meeting.objects.create(
            title=self.title,
            university=self.university,
            course=self.course,
            date_start=self.date_now,
            date_end=self.date_now,
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
        self.assertEquals(self.meeting1.university, self.university)
        self.assertEquals(self.meeting1.course, self.course)
        self.assertEquals(self.meeting1.date_start, self.date_now)
        self.assertEquals(self.meeting1.date_end, self.date_now)
        self.assertEquals(self.meeting1.location, self.location)
        self.assertEquals(self.meeting1.description, self.description)

    def test_meeting_members(self):
        self.assertEquals(self.meeting1.members.get(username=self.username), self.person)

    def test_user_meetings(self):
        self.assertEquals(self.person.user_meetings.get(title=self.title), self.meeting1)

