import datetime
from domain.decorators import *
from django.db.models import Q
from django.shortcuts import redirect, render
from domain.forms.employers_forms import *
from domain.general_functions import *
from domain.models import *


@employee_required
def applications_view(request, ordering='without_archive_by_new'):
    update_old_overdue()
    archive_statuses = ['completed', 'canceled', 'payment_received']
    ordering_mas = [
        'without_archive_by_new',
        'without_archive_by_final_date',
        'without_archive_by_first_name_of_employer',
    ]
    ordering_mas_archive = [
        'archive_by_new',
        'archive_by_final_date',
        'archive_by_first_name_of_employer',
    ]
    archive = False
    if ordering in ordering_mas:
        applications = Application.objects.exclude(
            Q(status__in=['completed', 'overdue', 'canceled']))
    elif ordering in ordering_mas_archive:
        applications = Application.objects.filter(
            Q(status__in=['completed', 'overdue', 'canceled']))
        archive = True
    else:
        applications = Application.objects.all()

    if ordering == ordering_mas[0] or ordering == ordering_mas_archive[0]:
        applications = applications.order_by('-date_of_application')
    elif ordering == ordering_mas[1] or ordering == ordering_mas_archive[1]:
        applications = applications.order_by('final_date')
    elif ordering == ordering_mas[2] or ordering == ordering_mas_archive[2]:
        applications = applications.select_related('customer').order_by('customer__last_name')
    else:
        applications = applications.order_by('-date_of_application')

    for application in applications:
        application.status_in_rus = get_russian_status(application.status)

    context = {
        'applications': applications,
        'archive': archive,
    }
    return render(request, 'employees_templates/employers/view/applications_view.html', context)


@employee_required
def application_detail_view(request, application_id):
    update_old_overdue()
    application = Application.objects.get(id=application_id)
    application.status_in_rus = get_russian_status(application.status)
    if request.method == 'POST':
        form = ChangeStateOfApplicationForm(request.POST, instance=application)
        if form.is_valid():
            status = form.cleaned_data['status']
            if status == 'in_progress':
                application.status = status
                application.employee = Employee.objects.get(id=request.user.id)
            if status == 'canceled':
                application.date_of_cancellation = datetime.datetime.today()
                application.status = status
            elif status == 'completed' or status == 'payment_received':
                application.date_of_completion = datetime.datetime.today()
                application.status = status
            else:
                application.date_of_completion = None
                application.date_of_cancellation = None
                application.status = status
            application.date_of_last_change = datetime.datetime.now()
            application.save()
            return redirect('applications_view_detail', application_id=application.id)
    else:
        form = ChangeStateOfApplicationForm(instance=application)
    application_responses = ApplicationsResponses.objects.filter(application_id=application_id)
    for response in application_responses:
        response.status_in_rus = get_russian_status_in_responses(response.status)
        response.interviews = JobInterview.objects.filter(application_response=response)
        for interview in response.interviews:
            interview.status_in_rus = get_russian_status_interview(interview.status)
    context = {
        'application': application,
        'application_responses': application_responses,
        'form': form,
    }
    return render(request, 'employees_templates/employers/view/application_view_detail.html', context)


@employee_required
def job_seeker_filter_for_application(request, application_id):
    update_old_overdue()
    application = Application.objects.get(id=application_id)
    application_responses = ApplicationsResponses.objects.filter(application_id=application_id)
    added_job_seeker_ids = application_responses.values_list('job_seeker__id', flat=True)
    job_seekers = JobSeeker.objects.exclude(id__in=added_job_seeker_ids)
    for job_seeker in job_seekers:
        job_seeker.matching_result = calculate_matching_between_job_seeker_and_application(job_seeker, application)

    job_seekers = sorted(job_seekers, key=lambda x: x.matching_result, reverse=True)
    job_seekers = [job_seeker for job_seeker in job_seekers if job_seeker.matching_result >= 50]

    context = {
        'application': application,
        'application_responses': application_responses,
        'job_seekers': job_seekers
    }
    return render(request, 'employees_templates/employers/view/job_seekers_filter.html', context)


@employee_required
def add_job_seeker_for_application(request, application_id, job_seeker_id):
    update_old_overdue()
    application_response = ApplicationsResponses.objects.create(
        application_id=application_id,
        job_seeker_id=job_seeker_id,
        evaluation=calculate_matching_between_job_seeker_and_application(JobSeeker.objects.get(id=job_seeker_id),
                                                                         Application.objects.get(id=application_id)),
        status='pending'
    )
    application_response.save()
    return redirect(request.META.get('HTTP_REFERER', None))
