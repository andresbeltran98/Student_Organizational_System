from django import forms
from ..models import Meeting
from django.contrib.admin import widgets


class CreateMeetingForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateMeetingForm, self).__init__(*args, **kwargs)
        self.fields['date_start'].label = 'Start date/time'
        self.fields['date_end'].label = 'End date/time'

    class Meta:
        model = Meeting
        fields = ['title', 'university', 'course', 'date_start', 'date_end', 'location', 'description']