from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Meeting(models.Model):

    title = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(User, through='Membership', related_name='user_meetings', default=None)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # returns the path as a string
        return reverse('meeting-detail', kwargs={'pk': self.pk})


class Membership(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    date_joined = models.DateField()
    is_organizer = models.BooleanField(default=False)
