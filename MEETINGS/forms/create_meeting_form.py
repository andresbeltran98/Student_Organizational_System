from django import forms
from ..models import Meeting


class CreateMeetingForm(forms.ModelForm):
    """
    This class represents the form used to create a new Meeting instance
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor
        :param args: arguments
        :param kwargs: additional arguments
        """
        super(CreateMeetingForm, self).__init__(*args, **kwargs)
        self.fields['date_start'].label = 'Start date/time'
        self.fields['date_end'].label = 'End date/time'

    class Meta:
        """
        Fields to be displayed in the form
        """
        model = Meeting
        fields = ['title', 'university', 'course', 'date_start', 'date_end', 'location', 'description']