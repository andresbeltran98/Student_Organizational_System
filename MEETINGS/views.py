from django.shortcuts import render

def create_meeting(request):
    return render(request, 'Meetings/meeting_form.html')
