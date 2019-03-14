from django.urls import path
from .views import (MeetingListView, MeetingDetailView, MeetingCreateView,
                    MeetingUpdateView, MeetingDeleteView, SearchListView)
from . import views

urlpatterns = [
    path('', MeetingListView.as_view(), name='meetings-list'),
    path('create/', MeetingCreateView.as_view(), name='meeting-create'),
    path('search/', SearchListView.as_view(), name='meeting-search'),
    path('meeting/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
    path('meeting/<int:pk>/update/', MeetingUpdateView.as_view(), name='meeting-update'),
    path('meeting/<int:pk>/delete/', MeetingDeleteView.as_view(), name='meeting-delete'),

]
