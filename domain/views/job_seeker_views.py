from datetime import timedelta
from datetime import datetime as dt
from django import forms
from django.shortcuts import redirect, render
from domain.forms.job_seekers_forms import *
from domain.models import *


def job_seeker_create_view(request):
    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES)
        if form.is_valid():
            job_seeker = form.save()
            return redirect('home')
    else:
        form = JobSeekerForm()
    context = {
        'form': form,
    }
    return render(request, 'job_seekers/create/job_seekers_create.html', context)