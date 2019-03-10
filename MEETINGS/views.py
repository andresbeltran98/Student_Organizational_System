from django.shortcuts import render

def create_meeting(request):
    return render(request, 'Meeting/meeting_form.html')
