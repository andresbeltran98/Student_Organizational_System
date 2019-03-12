from django.urls import path
from .views import MeetingListView, MeetingDetailView, MeetingCreateView
from . import views

urlpatterns = [
    path('', MeetingListView.as_view(), name='meetings-list'),
    path('meeting/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('create/', MeetingCreateView.as_view(), name='meeting-create'),
]
