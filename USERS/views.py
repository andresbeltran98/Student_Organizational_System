from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.university = form.cleaned_data.get('university')
            user.profile.major = form.cleaned_data.get('major')
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'USERS/register.html', {'form': form})


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'USERS/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
