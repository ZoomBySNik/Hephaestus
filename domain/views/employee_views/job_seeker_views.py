from datetime import timedelta, date
from datetime import datetime as dt
from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from domain.general_functions import *
from domain.decorators import *
from domain.forms.job_seekers_forms import *
from domain.models import *


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
            return redirect('applications_view_detail', application_response.application.id)
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
            if form.cleaned_data['locality']:
                address = get_or_create_address(form.cleaned_data['locality'],
                                                form.cleaned_data['street'],
                                                form.cleaned_data['number_of_building'],
                                                form.cleaned_data['apartment_number'])
                link = None
            else:
                link = form.cleaned_data['link']
                address = None
            interview = JobInterview.objects.create(
                application_response=application_response,
                employee=form.cleaned_data['employee'],
                date_of_interview=form.cleaned_data['date_of_interview'],
                description='',
                address=address,
                link=link
            )
            interview.save()
            application_response.status = 'under_review'
            application = application_response.application
            application.date_of_last_change = datetime.datetime.now()
            application.save()
            application_response.save()
            return redirect('home')
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


def create_interview_feedback(request, interview_id):
    update_old_overdue()
    interview = JobInterview.objects.get(id=interview_id)
    response = interview.application_response
    if request.method == 'POST':
        form = ReviewOnInterviewForm(request.POST)
        if form.is_valid():
            response.status = form.cleaned_data['response_status']
            interview.description = form.cleaned_data['interview_description']
            interview.status = 'with_feedback'
            response.save()
            application = interview.application_response.application
            application.save()
            interview.save()
            return redirect(request.META.get('HTTP_REFERER', None))
    else:
        form = ReviewOnInterviewForm()
    context = {
        'form': form,
        'application_response': response
    }
    return render(request, 'employees_templates/interviews/review_on_interview.html', context)


@employee_required
def document_required_in_confirmation_view(request, document_confirmation_id):
    document_confirmation = get_object_or_404(DocumentConfirmation, id=document_confirmation_id)

    # Проверяем, связан ли документ с образованием или опытом работы
    if document_confirmation.educationofjobseeker_set.exists():
        # Документ связан с образованием
        education_instance = EducationOfJobSeeker.objects.get(document_confirmation=document_confirmation)
        flag = 'education'
        context = {'unconfirmed': education_instance}
    elif document_confirmation.workexperience_set.exists():
        # Документ связан с опытом работы
        work_experience_instance = WorkExperience.objects.get(document_confirmation=document_confirmation)
        flag = 'work_experience'
        context = {'unconfirmed': work_experience_instance}
    context['flag'] = flag
    return render(request, 'employees_templates/job_seekers/confirmation/confirmation.html', context)


@employee_required
def document_confirm_view(request, document_confirmation_id):
    document_confirmation = get_object_or_404(DocumentConfirmation, id=document_confirmation_id)
    document_confirmation.confirmation = True
    document_confirmation.save()
    return redirect('home')


@employee_required
def document_reject_view(request, document_confirmation_id):
    document_confirmation = get_object_or_404(DocumentConfirmation, id=document_confirmation_id)
    document_confirmation.confirmation = False
    document_confirmation.save()
    return redirect('home')
