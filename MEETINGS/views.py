import datetime
from django.shortcuts import render, redirect, reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import Meeting, Membership
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django import forms
from django.db.models import Q
from .forms.share_form import ShareForm
from .forms.create_meeting_form import CreateMeetingForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView
)
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from CALENDAR.utils import Calendar, get_date, prev_month, next_month
from django.utils.safestring import mark_safe
import django_filters


class MeetingCreateView(LoginRequiredMixin, CreateView):
    """ This class loads the form used for creating a new Meeting instance
    Attributes:
        model = the Meeting database
        form_class = The form used for creating a meeting
    """
    model = Meeting
    form_class = CreateMeetingForm

    def form_valid(self, form):
        """ The form is valid. Saves the instance on the database and sets the user who created the meeting
        as the organizer
        :param form: The form filled out by the user
        :return: A valid form
        """
        self.object = form.save(commit=False)
        self.object.save()
        create_membership(self.request.user, self.object, True)
        return super().form_valid(form)


class MeetingListView(LoginRequiredMixin, ListView):
    """ This class retrieves and displays all the user's meetings
    Attributes:
        template_name: the html template that displays the meetings to the user
    """
    template_name = 'MEETINGS/meeting_list.html'

    def get_context_data(self, **kwargs):
        """ Passes the current context(objects) to the template
        :param kwargs: optional arguments
        :return: Dictionary containing keys used by the template
        """
        context = super().get_context_data(**kwargs)
        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate our calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        events = self.request.user.user_meetings.filter(date_start__year=d.year, date_start__month=d.month)
        html_cal = cal.formatmonth(events, withyear=True)

        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        context['calendar'] = mark_safe(html_cal)
        return context

    def get_queryset(self):
        return self.request.user.user_meetings.all()


class MeetingDetailView(LoginRequiredMixin, FormMixin, DetailView):
    """ This class represents a Meeting page
    Attributes:
        model: the model (database) used for each detail page
        template_name: the html template to be loaded
        form_class: required by FormMixin
    """
    model = Meeting
    template_name = 'MEETINGS/meeting_detail.html'
    form_class = forms.Form

    def get_context_data(self, **kwargs):
        """ Passes the current context(objects) to the template
        :param kwargs: optional arguments
        :return: Dictionary containing keys used by the template
        """
        context = super().get_context_data(**kwargs)
        is_member = False
        is_organizer = False

        try:
            self.object.members.get(username=self.request.user.username)
            is_member = True
            membership = Membership.objects.get(group=self.get_object(), person=self.request.user)
            is_organizer = membership.is_organizer
        except ObjectDoesNotExist:
            print("Member not in meeting")

        share_form = ShareForm()

        context['form'] = share_form
        context['is_member'] = is_member
        context['is_organizer'] = is_organizer

        return context

    def post(self, request, *args, **kwargs):
        """ Handles the user Post requests
        :param request: The current Post request
        :param args: optional arguments passed by request
        :param kwargs: extra arguments
        :return:
        """
        meeting = self.get_object()

        if request.POST.get('join_meeting'):
            # A user joins a meeting
            create_membership(request.user, meeting, False)
            return redirect(meeting.get_absolute_url())

        if request.POST.get('leave_meeting_mem'):
            # An attendee leaves the meeting
            membership = Membership.objects.get(group=meeting, person=request.user)
            membership.delete()
            return redirect(meeting.get_absolute_url())

        if request.POST.get('leave_meeting_org'):
            # The organizer leaves the meeting: select a new organizer and remove membership
            new_organizer_username = request.POST['select_org']
            new_org = User.objects.get(username=new_organizer_username)
            new_membership = Membership.objects.get(group=meeting, person=new_org)
            new_membership.is_organizer = True
            new_membership.save()
            old_membership = Membership.objects.get(group=meeting, person=request.user)
            old_membership.delete()
            return redirect(meeting.get_absolute_url())

        if request.is_ajax():
            # Ajax request
            data = json.load(request)
            post_name = data['name']

            if post_name == 'share_form':
                # The user shares the meeting
                share_form = ShareForm(data=data['form'])
                if share_form.is_valid():
                    recipients = share_form.clean()['emails']
                    send_invitations(recipients, request.user.username, meeting.title, meeting.get_absolute_url())
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'error': share_form.errors})

            if post_name == 'leave_form':
                # A member leaves a meeting
                if meeting.members.count() > 1:
                    return JsonResponse({'select': True})
                else:
                    return JsonResponse({'select': False})


class MeetingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ This class displays and processes the form used for updating the meeting details
    Attributes:
        model = the Meeting database
        fields = the fields to be updated
    """
    model = Meeting
    fields = ['title', 'university', 'course', 'date_start', 'date_end', 'location', 'description']

    def form_valid(self, form):
        """ The form is valid. Saves the changes on the database
        :param form: The form filled out by the user to update the fields
        :return: The current form
        """
        form.save()
        return super().form_valid(form)

    def test_func(self):
        """ Checks who can update the meeting details
        :return: True if the user is the meeting organizer. False otherwise
        """
        membership = Membership.objects.get(group=self.get_object(), person=self.request.user)
        if membership.is_organizer:
            return True
        return False


class MeetingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ This class manages the deletion of a Meeting instance
    Attributes:
        model = the Meeting database
    """
    model = Meeting

    def get_success_url(self):
        """ Returns the url to which the user will be redirected after deleting an instance
        :return: redirection url
        """
        return reverse('meetings-list')

    def test_func(self):
        """ Checks who can delete the current meeting
        :return: True if the user is the meeting organizer. False otherwise
        """
        membership = Membership.objects.get(group=self.get_object(), person=self.request.user)
        if membership.is_organizer:
            return True
        return False


class SearchListView(LoginRequiredMixin, ListView):
    """ This class manages the meeting Search engine
    Attributes:
        template_name: the html form that loads the search engine
    """
    template_name = 'MEETINGS/search_list.html'


    def get_queryset(self):
        """ Retrieves the meeting objects depending on the user query
        :return: A list of meetings that match the user query
        """

        if self.request.is_ajax():
            query = self.request.GET['search_text']
            results = None
            if query is not None:
                results = Meeting.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            return results

        else:
            query = self.request.GET
            meeting_filter = MeetingSearchFilter(query, queryset=Meeting.objects.all())
            # results = None
            # if query is not None:
                # results = Meeting.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
            # return results
            return meeting_filter.qs

    def get_context_data(self, **kwargs):
        """ Passes the current context(objects) to the template
        :param kwargs: optional arguments
        :return: Dictionary containing keys used by the template
        """
        context = super().get_context_data(**kwargs)
        context['filter'] = MeetingSearchFilter()
        return context


class MeetingSearchFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    university = django_filters.CharFilter(lookup_expr='icontains')
    course = django_filters.CharFilter(lookup_expr='icontains')
    location = django_filters.CharFilter(lookup_expr='icontains')
    date_start = django_filters.DateFilter(lookup_expr='date')

    def __init__(self, *args, **kwargs):
        super(MeetingSearchFilter, self).__init__(*args, **kwargs)
        self.filters['date_start'].label = "Date"

    class Meta:
        model = Meeting
        fields = ['title', 'university', 'course', 'date_start', 'location']


def create_membership(user, meeting, is_organizer):
    """ Creates a new Membership instance (User-Meeting relationship) and saves it on the Membership database
    :param user: the User who is logged in
    :param meeting: the meeting instance that User joins
    :param is_organizer: True if User is the organizer
    """

    m1 = Membership(person=user, group=meeting,
                    date_joined=datetime.datetime.now().date(), is_organizer=is_organizer)
    m1.save()


def send_invitations(recipients_list, username, meeting_name, link_meeting):
    """ Sends invitations emails after the user clicks on "Share meeting"
    Args:
        recipients_list: the list of recipients emails
        username: the current user
        meeting_name: the name of the current meeting
        link_meeting: the link to the meeting
    """

    subject = "Invitation to a Study Session"
    message = "{} has invited you to the study session \"{}\"\n" \
              "The link to the meeting is: http://127.0.0.1:8000{}".format(username, meeting_name, link_meeting)
    from_email = settings.EMAIL_HOST_USER
    recipients = recipients_list
    send_mail(subject=subject,
              from_email=from_email,
              recipient_list=recipients,
              message=message,
              fail_silently=False)