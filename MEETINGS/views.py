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
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


def create_membership(request, meeting, organizer):
    m1 = Membership(person=request.user, group=meeting,
                    date_joined=datetime.datetime.now().date(), is_organizer=organizer)
    m1.save()

def send_invitations(recipients_list, username, meeting_name, link_meeting):
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


class MeetingCreateView(LoginRequiredMixin, CreateView):
    model = Meeting
    fields = ['title', 'university', 'course', 'date', 'location', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        create_membership(self.request, self.object, True)
        return super().form_valid(form)


class MeetingListView(LoginRequiredMixin, ListView):
    template_name = 'MEETINGS/meeting_list.html'

    def get_queryset(self):
        return self.request.user.user_meetings.all()


class MeetingDetailView(LoginRequiredMixin, FormMixin, DetailView):
    model = Meeting
    template_name = 'MEETINGS/meeting_detail.html'
    form_class = forms.Form



    def get_context_data(self, **kwargs):
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

        context['is_member'] = is_member
        context['is_organizer'] = is_organizer

        return context

    def post(self, request, *args, **kwargs):
        meeting = self.get_object()
        if request.POST.get('join_meeting'):
            create_membership(request, meeting, False)
            return redirect(meeting.get_absolute_url())

        if request.POST.get('leave_meeting'):
            membership = Membership.objects.get(group=meeting, person=request.user)
            membership.delete()
            return redirect(meeting.get_absolute_url())

        if request.POST.get('share_meeting'):
            share_form = ShareForm()
            context = {
                'form' : share_form
            }
            return render(request, 'MEETINGS/share_meeting.html', context)

        if request.POST.get('send_invitations'):
            share_form = ShareForm(request.POST)
            if share_form.is_valid():
                recipients = share_form.clean()['emails']
                messages.success(request, "The invitations were sent successfully!")
                send_invitations(recipients, request.user.username, meeting.title, meeting.get_absolute_url())
                return redirect(meeting.get_absolute_url())
            else:
                share_form = ShareForm()
                context = {
                    'form': share_form
                }
                messages.error(request, "Invalid email(s)")
                return render(request, 'MEETINGS/share_meeting.html', context)


class MeetingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Meeting
    fields = ['title', 'university', 'course', 'date', 'location', 'description']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def test_func(self):
        membership = Membership.objects.get(group=self.get_object(), person=self.request.user)
        if membership.is_organizer:
            return True
        return False


class MeetingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Meeting

    def get_success_url(self):
        return reverse('meetings-list')

    def test_func(self):
        membership = Membership.objects.get(group=self.get_object(), person=self.request.user)
        if membership.is_organizer:
            return True
        return False


class SearchListView(LoginRequiredMixin, ListView):
    template_name = 'MEETINGS/search_list.html'

    def get_queryset(self):
        query = self.request.GET.get('myquery')
        results = None
        if query is not None:
            results = Meeting.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return results