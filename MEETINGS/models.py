from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Meeting(models.Model):
    """ This class represent a Study Session:
    Attributes:
        title: The meeting title
        university: The university at which the meeting will be held
        course: The course name/number which the session will focus on
        date_start: The start date/time
        date_end: The end date/time
        location: The location of the meeting
        description: A brief description on the purpose and topics of the meeting
        members: The meeting attendees (Many-to-many relationship)
    """

    title = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, through='Membership', related_name='user_meetings', default=None)

    def __str__(self):
        return self.title

    @property
    def get_html_url(self):
        """ Returns the url of this meeting in html format
        :return: the html url
        """
        url = reverse('meeting-detail', kwargs={'pk': self.pk})
        return f'<a href="{url}"> {self.title} </a>'

    @property
    def get_time_format(self):
        """ Returns datetime fields in hour:minute format
        :return: dates in hour:minute format
        """
        return self.date_start.strftime('%H:%M')

    def get_absolute_url(self):
        """ Returns the path/url of this meeting as a string
        :return: the path/url of this meeting as a string
        """
        return reverse('meeting-detail', kwargs={'pk': self.pk})


class Membership(models.Model):
    """ This class represent a Meeting-User membership
    Attributes:
        person: The current user
        group: A meeting to which the user belongs
        date_joined: The date when the user joined the meeting
        is_organizer: True if the user is the meeting organizer. False otherwise
    """
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    date_joined = models.DateField()
    is_organizer = models.BooleanField(default=False)
