import datetime
from django.db.models import Q
from django.shortcuts import redirect, render
from domain.forms.employers_forms import *
from domain.models import *


def organization_create_view(request, *args, **kwargs):
    organizations_list = Organization.objects.order_by('name')
    form_type = 'organization'
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            address = Address.objects.create(
                locality=form.cleaned_data['locality'],
                street=form.cleaned_data['street'],
                number_of_building=form.cleaned_data['number_of_building'],
                apartment_number=form.cleaned_data['apartment_number'],
            )
            organization = form.save(commit=False)
            organization.address = address
            organization.save()
            return redirect('employers_create', organization.id)
    else:
        form = OrganizationForm()
    context = {
        'form_type': form_type,
        'form': form,
        'organizations': organizations_list
    }
    return render(request, 'employers/create/organization_create.html', context)


def employers_create_view(request, organization_id):
    organization = Organization.objects.get(id=organization_id)
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.organization = Organization.objects.get(id=organization_id)
            employer = form.save()
            return redirect('application_create', employer_id=employer.id)
    else:
        form = EmployerForm()
    employers = Employer.objects.order_by('surname').filter(organization_id=organization_id)
    context = {
        'form': form,
        'employers': employers,
        'organization': organization,
    }
    return render(request, 'employers/create/employers_create.html', context)


def application_create_view(request, employer_id):
    employer = Employer.objects.get(id=employer_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            employee = Employee.objects.get(id=request.user.id)
            application = form.save(commit=False)
            application.employer = employer
            application.employee = employee
            application.save()
            form.save_m2m()

            return redirect('home')
    else:
        form = ApplicationForm()
    context = {
        'employer': employer,
        'form': form
    }
    return render(request, 'employers/create/application_create.html', context)


def get_russian_status(status):
    status_dict = {
        'new': 'Новая',
        'in_progress': 'В обработке',
        'pending_approval': 'На согласовании',
        'completed': 'Завершена',
        'canceled': 'Отменена',
        'payment_received': 'Получена оплата'
    }
    return status_dict.get(status)


def applications_view(request, ordering='without_archive_by_new'):
    archive_statuses = ['completed', 'canceled', 'payment_received']
    ordering_mas = [
        'without_archive_by_new',
        'without_archive_by_final_date',
        'without_archive_by_surname_of_employer',
    ]
    ordering_mas_archive = [
        'archive_by_new',
        'archive_by_final_date',
        'archive_by_surname_of_employer',
    ]

    if ordering in ordering_mas:
        applications = Application.objects.exclude(
            Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))
    elif ordering in ordering_mas_archive:
        applications = Application.objects.filter(
            Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))
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
    }
    return render(request, 'employers/view/applications_view.html', context)


def get_russian_status_in_responses(status):
    status_dict = {
        'pending': 'В ожидании',
        'under_review': 'Рассмотрение',
        'accepted': 'Принят',
        'rejected': 'Отклонен',
        'withdrawn': 'Отозван',
    }
    return status_dict.get(status)


def application_detail_view(request, application_id):
    application = Application.objects.get(id=application_id)
    application.status_in_rus = get_russian_status(application.status)
    if request.method == 'POST':
        form = ChangeStateOfApplicationForm(request.POST, instance=application)
        if form.is_valid():
            status = form.cleaned_data['status']
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
            application.save()
            return redirect('applications_view_detail', application_id=application.id)
    else:
        form = ChangeStateOfApplicationForm(instance=application)
    application_responses = ApplicationsResponses.objects.filter(application_id=application_id)

    for response in application_responses:
        response.status_in_rus = get_russian_status_in_responses(response.status)
    context = {
        'application': application,
        'application_responses': application_responses,
        'form': form,
    }
    return render(request, 'employers/view/application_view_detail.html', context)


def calculate_matching_between_job_seeker_and_application(job_seeker, application):
    educations = job_seeker.educationofjobseeker_set.all()
    education_factor = 0
    for education in educations:
        if education.education.education_level.code >= application.education_level.code:
            education_factor = 1

    specializations = job_seeker.specialization.all()
    specialization_factor = 0
    for specialization in specializations:
        if specialization == application.specialization:
            specialization_factor = 1

    work_experiences = job_seeker.workexperience_set.all()
    work_experiences_years = 0
    for work_experience in work_experiences:
        date_of_employment = work_experience.date_of_employment
        date_of_dismissal = work_experience.date_of_dismissal
        if date_of_dismissal == None:
            date_of_dismissal = datetime.datetime.today()
        years_worked = date_of_dismissal.year - date_of_employment.year
        if work_experience.position == application.position:
            work_experiences_years += years_worked
        else:
            work_experiences_years += years_worked * 0.2
    work_experiences_years = work_experiences_years
    if work_experiences_years >= application.experience:
        experience_factor = 1
    else:
        experience_factor = work_experiences_years / application.experience

    skills = job_seeker.skill.all()
    count_of_skills = len(application.skills.all())
    if count_of_skills == 0:
        skill_factor = 1
    else:
        skill_factor = 0
        for skill in skills:
            if skill in application.skills.all():
                skill_factor += 1
        skill_factor = skill_factor / count_of_skills

    software_and_hardware_tools = job_seeker.softwareandhardwaretoolofjobseeker_set.all()
    count_of_software_and_hardware_tools = len(application.software_and_hardware_tools.all())
    if count_of_software_and_hardware_tools == 0:
        software_and_hardware_tool_factor = 1
    else:
        software_and_hardware_tool_factor = 0
        for software_and_hardware_tool in software_and_hardware_tools:
            if software_and_hardware_tool.software_and_hardware_tool in application.software_and_hardware_tools.all():
                software_and_hardware_tool_factor += 1
        software_and_hardware_tool_factor = software_and_hardware_tool_factor / count_of_software_and_hardware_tools

    percent = education_factor * specialization_factor * experience_factor * skill_factor * software_and_hardware_tool_factor * 100
    return percent


def job_seeker_filter_for_application(request, application_id):
    application = Application.objects.get(id=application_id)
    application_responses = ApplicationsResponses.objects.filter(application_id=application_id)
    added_job_seeker_ids = application_responses.values_list('job_seeker__id', flat=True)
    job_seekers = JobSeeker.objects.exclude(id__in=added_job_seeker_ids)
    for job_seeker in job_seekers:
        job_seeker.matching_result = calculate_matching_between_job_seeker_and_application(job_seeker, application)

    job_seekers = sorted(job_seekers, key=lambda x: x.matching_result, reverse=True)
    job_seekers = [job_seeker for job_seeker in job_seekers if job_seeker.matching_result >= 60]

    context = {
        'application': application,
        'application_responses': application_responses,
        'job_seekers': job_seekers
    }
    return render(request, 'employers/view/job_seekers_filter.html', context)


def add_job_seeker_for_application(request, application_id, job_seeker_id):
    application_response = ApplicationsResponses.objects.create(
        application_id=application_id,
        job_seeker_id=job_seeker_id,
        evaluation=calculate_matching_between_job_seeker_and_application(JobSeeker.objects.get(id=job_seeker_id),
                                                                         Application.objects.get(id=application_id)),
        status='pending'
    )
    application_response.save()
    return redirect(request.META.get('HTTP_REFERER', None))
