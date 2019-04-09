from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES, validate_email, ValidationError
from django.forms.fields import CharField


class CommaSeparatedEmailField(CharField):
    """
    This class represents a field used for validating multiple emails separated by commas
    """

    def __init__(self, *args, **kwargs):
        """ Initializes the current field and passes arguments to its parent class
        """
        self.token = kwargs.pop("token", ",")
        super(CommaSeparatedEmailField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        """ Parses the user input and returns a list of strings containing emails
        :param value: The user input
        :return: A list of strings containing emails
        """
        if value in EMPTY_VALUES:
            return []

        value = [item.strip() for item in value.split(self.token) if item.strip()]

        return list(set(value))

    def clean(self, value):
        """ Check that the field contains one or more 'comma-separated' emails
        and normalizes the data to a list of the email strings.
        :param value: The user input
        :return: A list of validated emails
        """
        value = self.to_python(value)

        for email in value:
            try:
                validate_email(email)
            except ValidationError:
                raise forms.ValidationError(_(u"'%s' is not a valid e-mail address.") % email)

        return value


class ShareForm(forms.Form):
    """ This class represents the form used for sharing a meeting
    Attributes:
        emails: the recipients' emails (separated by commas)
    """
    emails = CommaSeparatedEmailField(
     widget=forms.Textarea(attrs={'placeholder': 'E-mail address(es)'}),
     label=_(u'')
    )




