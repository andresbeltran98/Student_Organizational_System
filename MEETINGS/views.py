from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView
)

from .models import Meeting, Membership
import datetime
from django.contrib.auth.models import User


def create_membership(request, meeting):
    m1 = Membership(person=User.objects.first(), group=meeting,
                    date_joined=datetime.datetime.now().date(), is_organizer=True)
    # use request.user in person=
    m1.save()


class MeetingCreateView(CreateView):
    model = Meeting
    fields = ['title', 'university', 'course', 'date', 'location', 'description']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        create_membership(self.request, self.object)
        return super().form_valid(form)


class MeetingListView(ListView):
    queryset = User.objects.first().user_meetings.all()
    template_name = 'MEETINGS/meeting_list.html'


class MeetingDetailView(DetailView):
    model = Meeting
    template_name = 'MEETINGS/meeting_detail.html'



