from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    university = models.CharField(max_length=50, default="No University")
    major = models.CharField(max_length=20, default="Undecided")

    def get_absolute_url(self):
        # returns the path as a string
        return reverse('profile', kwargs={'pk': self.pk})

    def __str__(self):
        return f'{self.user.username} Profile'
