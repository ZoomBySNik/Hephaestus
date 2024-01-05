from datetime import timedelta, date
from datetime import datetime as dt
from django import forms
from django.shortcuts import redirect, render
from domain.forms.job_seekers_forms import *
from domain.models import *


def job_seeker_create_view(request):
    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES)
        if form.is_valid():
            address = Address.objects.create(
                locality=form.cleaned_data['locality'],
            )
            job_seeker = form.save(commit=False)
            job_seeker.address = address
            job_seeker.save()
            return redirect('job_seeker_view', job_seeker_id=job_seeker.id)
    else:
        form = JobSeekerForm()
    context = {
        'form': form,
    }
    return render(request, 'job_seekers/create/job_seekers_create.html', context)


def job_seeker_view(request, job_seeker_id):
    job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    job_seeker.age = (date.today() - job_seeker.birthdate) // timedelta(days=365.2425)
    context = {
        'job_seeker': job_seeker,
    }
    return render(request, 'job_seekers/view/job_seeker_view.html', context)


def skills_view(request, job_seeker_id):
    job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            job_seeker.skill.set(form.cleaned_data['skills'])
            job_seeker.save()
            return redirect('job_seeker_view', job_seeker_id=job_seeker.id)
    else:
        form = SkillsForm()

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers/create/skills_create.html', context)


def specialization_view(request, job_seeker_id):
    job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        if form.is_valid():
            job_seeker.specialization.set(form.cleaned_data['specializations'])
            job_seeker.save()
            return redirect('job_seeker_view', job_seeker_id=job_seeker.id)
    else:
        form = SpecializationForm()

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers/create/specialization_create.html', context)


def software_and_hardware_tools_view(request, job_seeker_id):
    job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    if request.method == 'POST':
        form = SoftwareAndHardwareToolForm(request.POST)
        if form.is_valid():
            tools = SoftwareAndHardwareToolOfJobSeeker.objects.filter(job_seeker=job_seeker)
            tools.delete()
            for tool in form.cleaned_data['software_and_hardware_tools']:

                software_and_hardware_tools_of_job_seeker = SoftwareAndHardwareToolOfJobSeeker.objects.create(
                    job_seeker=job_seeker,
                    software_and_hardware_tool=tool
                )
                software_and_hardware_tools_of_job_seeker.save()
            return redirect('job_seeker_view', job_seeker_id=job_seeker.id)
    else:
        form = SoftwareAndHardwareToolForm()

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers/create/software_and_hardware_tools_create.html', context)
