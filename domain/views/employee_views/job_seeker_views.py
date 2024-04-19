from datetime import timedelta, date
from datetime import datetime as dt
from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from domain.general_functions import *
from domain.decorators import *
from domain.forms.job_seekers_forms import *
from domain.models import *


@employee_required
def job_seeker_create_view(request, job_seeker_id=None):
    job_seeker = get_object_or_404(JobSeeker, id=job_seeker_id) if job_seeker_id else None
    if job_seeker and job_seeker.birthdate:
        job_seeker.birthdate = job_seeker.birthdate.strftime('%Y-%m-%d')
    if request.method == 'POST':
        form = JobSeekerForm(request.POST, request.FILES, instance=job_seeker)
        if form.is_valid():
            # Перед сохранением формы, создадим адрес, если его еще нет
            address_data = {
                'locality': form.cleaned_data['locality'],
                # Добавьте другие поля адреса по необходимости
            }
            addresses = Address.objects.filter(**address_data)

            if addresses.exists():
                address = addresses.first()
            else:
                address = Address.objects.create(**address_data)

            job_seeker = form.save(commit=False)
            job_seeker.address = address
            job_seeker.save()

            return redirect('job_seeker_view', job_seeker_id=job_seeker.id)
    else:
        # Если job_seeker_id передан, заполним форму существующими данными
        form = JobSeekerForm(instance=job_seeker) if job_seeker else JobSeekerForm()
        if job_seeker_id:
            form.initial['locality'] = job_seeker.address.locality
    context = {
        'form': form,
    }
    return render(request, 'employees_templates/job_seekers/create/job_seekers_create.html', context)


@employee_required
def job_seeker_all_view(request):
    job_seekers = JobSeeker.objects.all()
    context = {
        'job_seekers': job_seekers,
    }
    return render(request, 'employees_templates/job_seekers/view/job_seekers_all_view.html', context)


@employee_required
def job_seeker_view(request, job_seeker_id):
    job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    if job_seeker.birthdate:
        job_seeker.age = (date.today() - job_seeker.birthdate) // timedelta(days=365.2425)
    else:
        job_seeker.age = None
    work_experiences = job_seeker.workexperience_set.all().order_by('-date_of_employment')
    context = {
        'job_seeker': job_seeker,
        'work_experiences': work_experiences,
    }
    return render(request, 'employees_templates/job_seekers/view/job_seeker_view.html', context)


@employee_required
def reject_job_seeker_response(request, application_response_id):
    update_old_overdue()
    application_response = ApplicationsResponses.objects.get(id=application_response_id)
    if request.method == 'POST':
        form = ApplicationResponseRejectForm(request.POST)
        if form.is_valid():
            application_response.description = form.cleaned_data['description']
            application_response.status = 'rejected'
            application_response.save()
            return redirect(request.META.get('HTTP_REFERER', None))
    else:
        form = ApplicationResponseRejectForm()
    context = {
        'application_response': application_response,
        'form': form
    }
    return render(request, 'employees_templates/responses/reject_response.html', context)


@employee_required
def invite_job_seeker_on_interview(request, application_response_id):
    update_old_overdue()
    application_response = ApplicationsResponses.objects.get(id=application_response_id)
    if request.method == 'POST':
        form = JobInterviewForm(request.POST)
        if form.is_valid():
            interview = JobInterview.objects.create(
                application_response=application_response,
                employee=form.cleaned_data['employee'],
                date_of_interview=form.cleaned_data['date_of_interview'],
                description=''
            )
            interview.save()
            application_response.status = 'under_review'
            application_response.save()
            return redirect(request.META.get('HTTP_REFERER', None))
    else:
        form = JobInterviewForm()
    context = {
        'application_response': application_response,
        'form': form
    }
    return render(request, 'employees_templates/interviews/invite_on_interview.html', context)


@employee_required
def employee_interviews_view(request, archive=0):
    update_old_overdue()
    employee = Employee.objects.get(id=request.user.id)
    if archive == 0:
        archive = False
        interviews = JobInterview.objects.all().filter(employee=employee).exclude(
            status__in=['rejected', 'with_feedback', 'overdue']).order_by('-date_of_interview')
    elif archive == 1:
        archive = True
        interviews = JobInterview.objects.all().filter(employee=employee).exclude(
            status__in=['pending', 'accepted', 'passed']).order_by('-date_of_interview')
    else:
        return redirect(request.META.get('HTTP_REFERER', None))


    for interview in interviews:
        interview.status_in_rus = get_russian_status_interview(interview.status)
    context = {
        'interviews': interviews,
        'archive': archive
    }
    return render(request, 'employees_templates/interviews/interviews.html', context)
