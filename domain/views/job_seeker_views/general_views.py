from datetime import timedelta, date
from datetime import datetime as dt
from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from domain.general_functions import *
from domain.decorators import *
from domain.forms.job_seekers_forms import *
from domain.models import *


@job_seeker_required
def skills_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            job_seeker.skill.set(form.cleaned_data['skills'])
            job_seeker.save()
            return redirect('user_profile')
    else:
        form = SkillsForm(initial={'skills': job_seeker.skill.all()})

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/skills_create.html', context)


@job_seeker_required
def specialization_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        if form.is_valid():
            job_seeker.specialization.set(form.cleaned_data['specializations'])
            job_seeker.save()
            return redirect('user_profile')
    else:
        form = SpecializationForm(initial={'specializations': job_seeker.specialization.all()})

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/specialization_create.html', context)


@job_seeker_required
def software_and_hardware_tools_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = SoftwareAndHardwareToolForm(request.POST)

        if form.is_valid():
            tools = SoftwareAndHardwareToolOfJobSeeker.objects.filter(job_seeker=job_seeker)
            tools.delete()

            for tool in form.cleaned_data['software_and_hardware_tools']:
                SoftwareAndHardwareToolOfJobSeeker.objects.create(
                    job_seeker=job_seeker,
                    software_and_hardware_tool=tool
                )

            return redirect('user_profile')
    else:
        selected_tools = SoftwareAndHardwareToolOfJobSeeker.objects.filter(job_seeker=job_seeker)

        initial_data = {
            'software_and_hardware_tools': selected_tools.values_list('software_and_hardware_tool', flat=True)}
        form = SoftwareAndHardwareToolForm(initial=initial_data)

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/software_and_hardware_tools_create.html', context)


@job_seeker_required
def job_seeker_education_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EducationForm(request.POST)
        if form.is_valid():
            address_data = {
                'locality': form.cleaned_data['education_organization_address_locality'],
                'street': form.cleaned_data['education_organization_address_street'],
                'number_of_building': form.cleaned_data['education_organization_address_street'],
            }
            addresses = Address.objects.filter(**address_data)

            if addresses.exists():
                address = addresses.first()
            else:
                address = Address.objects.create(**address_data)

            education_organization = EducationalOrganization(
                address=address,
                name=form.cleaned_data['education_organization_name']
            )
            education_organization.save()

            education = Education.objects.create(
                organization=education_organization,
                name=form.cleaned_data['name'],
                code=form.cleaned_data['code'],
                education_level=form.cleaned_data['education_level']
            )
            education.save()

            education_job_seeker = EducationOfJobSeeker.objects.create(
                job_seeker=job_seeker,
                education=education,
                year_received=form.cleaned_data['year_received']
            )
            education_job_seeker.save()
            return redirect('user_profile')
    else:
        form = EducationForm()

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/education_create.html', context)


@job_seeker_required
def job_seeker_work_experience_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience = WorkExperience.objects.create(
                job_seeker=job_seeker,
                organization=form.cleaned_data['organization'],
                position=form.cleaned_data['position'],
                date_of_employment=form.cleaned_data['date_of_employment'],
                date_of_dismissal=form.cleaned_data['date_of_dismissal']
            )
            work_experience.save()
            return redirect('user_profile')
    else:
        form = WorkExperienceForm()

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/work_experience.html', context)