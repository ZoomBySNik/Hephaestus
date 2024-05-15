from operator import attrgetter
from datetime import date
from datetime import datetime as dt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from domain.decorators import *
from domain.forms.employers_forms import EmployerForm
from domain.forms.general_forms import *
from domain.forms.job_seekers_forms import JobSeekerForm
from domain.models import *
from domain.general_functions import *


@login_required
def home_view(request):
    update_old_overdue()
    start_of_day = dt.combine(date.today(), dt.min.time())
    end_of_day = dt.combine(date.today(), dt.max.time())
    extra_data = {}
    if get_user_type(request.user.id) == 'job_seeker':
        job_seeker = get_user_data(request.user.id)
        applications = Application.objects.filter(
            ~Q(applicationsresponses__job_seeker_id=job_seeker.id) &
            ~(Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False)) &
            ~Q(status__in=['new', 'completed', 'overdue', 'canceled'])
        )
        filtered_applications = []
        if job_seeker.address:
            for application in applications:
                application.matching_result = calculate_matching_between_job_seeker_and_application(job_seeker,
                                                                                                    application)
                application.distance = haversine_distance(job_seeker.address.latitude, job_seeker.address.longitude,
                                                          application.employer.organization.address.latitude,
                                                          application.employer.organization.address.longitude)
                if application.matching_result >= 40 and (
                        application.distance < 50 or job_seeker.work_location_preference != 'local'):
                    filtered_applications.append(application)
            filtered_applications = sorted(filtered_applications, key=attrgetter('matching_result'), reverse=True)
        interviews_pending = JobInterview.objects.filter(
            Q(application_response__job_seeker=job_seeker) & Q(status='pending'))
        interviews_today = JobInterview.objects.filter(
            Q(application_response__job_seeker=job_seeker) &
            Q(status='accepted') &
            Q(date_of_interview__range=(start_of_day, end_of_day))
        )
        extra_data = {
            'applications': filtered_applications,
            'job_seeker': job_seeker,
            'interviews_pending': interviews_pending,
            'interviews_today': interviews_today,

        }
    if get_user_type(request.user.id) == 'employee':
        applications_by_new = Application.objects.all().order_by('-date_of_application').filter(
            status='new').exclude(
            Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))[:5]
        applications_by_final_date = Application.objects.all().order_by('final_date').filter(
            status__in=['new', 'in_progress', 'pending_approval']).exclude(
            Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))[:5]
        # Формируем временной промежуток для сегодняшнего дня
        interviews = JobInterview.objects.filter(date_of_interview__gte=start_of_day,
                                                 date_of_interview__lte=end_of_day,
                                                 status='accepted',
                                                 employee_id=request.user.id
                                                )
        for interview in interviews:
            interview.status_in_rus = get_russian_status_interview(interview.status)
        interviews_without_feedback = JobInterview.objects.filter(status='passed')
        for interview in interviews_without_feedback:
            interview.status_in_rus = get_russian_status_interview(interview.status)
        application_responses = ApplicationsResponses.objects.filter(status='pending').order_by('-evaluation')
        for application_response in application_responses:
            application_response.status_in_rus = get_russian_status_in_responses(application_response.status)
        unconfirmed_educations = EducationOfJobSeeker.objects.filter(document_confirmation__confirmation=None)
        unconfirmed_work_experiences = WorkExperience.objects.filter(document_confirmation__confirmation=None)
        extra_data = {
            'interviews': interviews,
            'interviews_without_feedback': interviews_without_feedback,
            'applications_by_new': applications_by_new,
            'applications_by_final_date': applications_by_final_date,
            'application_responses': application_responses,
            'unconfirmed_educations': unconfirmed_educations,
            'unconfirmed_work_experiences': unconfirmed_work_experiences,
        }

    response = {
        'extra_data': extra_data
    }
    return render(request, 'general_templates/home/home.html', response)


def error_view(request, error_message):
    context = {'error_message': error_message}
    return render(request, 'components/error.html', context)


def choose_user_type(request):
    return render(request, 'registration/select_user_type.html')


def registration(request, user_type):
    if request.method == 'POST':
        if user_type == 'employer':
            form = EmployerRegistrationForm(request.POST)
        elif user_type == 'job_seeker':
            form = JobSeekerRegistrationForm(request.POST)
        else:
            return redirect(request.META.get('HTTP_REFERER', None))
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

            return redirect('user_profile')
    else:
        if user_type == 'employer':
            form = EmployerRegistrationForm()
        elif user_type == 'job_seeker':
            form = JobSeekerRegistrationForm()
        else:
            return redirect(request.META.get('HTTP_REFERER', None))
    return render(request, 'registration/user_registration.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    user_type = get_user_type(user.id)
    data = get_user_data(user.id)
    if request.method == 'POST':
        form = PhotoSaveForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    else:
        form = PhotoSaveForm()
    context = {'user': user,
               'data': data,
               'user_type': user_type,
               'form': form}
    return render(request, 'general_templates/profile/profile.html', context)


@login_required
def profile_update(request):
    user = request.user
    user_type = get_user_type(user.id)
    data = get_user_data(user.id)
    if user_type == 'job_seeker':

        if request.method == 'POST':
            form = JobSeekerForm(request.POST, request.FILES, instance=data)
            if form.is_valid():
                if form.cleaned_data['locality']:
                    address = get_or_create_address(form.cleaned_data['locality'])
                    job_seeker = form.save(commit=False)
                    job_seeker.address = address
                    job_seeker.save()
                else:
                    form.save()
                return redirect('user_profile')
            else:
                return redirect('error_page', form.errors)
        else:
            form = JobSeekerForm(instance=data)
            if data.address:
                form.initial['locality'] = data.address.locality
    elif user_type == 'employer':
        if request.method == 'POST':
            form = EmployerForm(request.POST, request.FILES, instance=data)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
            else:
                return redirect('error_page', form.errors)
        else:
            form = EmployerForm(instance=data)
    elif user_type == 'employee':
        if request.method == 'POST':
            form = EmployeeForm(request.POST, request.FILES, instance=data)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
            else:
                return redirect('error_page', form.errors)
        else:
            form = EmployeeForm(instance=data)
    context = {'user': user,
               'data': data,
               'user_type': user_type,
               'form': form}
    return render(request, 'general_templates/profile/update_profile.html', context)


@login_required
def organization_view(request, organization_id):
    update_old_overdue()
    user_data = get_user_data(request.user.id)
    user_type = get_user_type(request.user.id)
    organization = Organization.objects.get(id=organization_id)
    is_member = False
    if user_type == 'employer':
        if user_data.organization_id == organization.id:
            is_member = True
    else:
        if user_type == 'employee':
            is_member = True
    is_job_seeker = False
    if user_type == 'job_seeker':
        is_job_seeker = True
    context = {
        'organization': organization,
        'is_member': is_member,
        'is_job_seeker': is_job_seeker,
    }
    if is_job_seeker:
        filtered_applications = []
        if user_data.address:
            applications = Application.objects.filter(
                Q(employer__organization=organization) &
                (~Q(applicationsresponses__job_seeker_id=user_data.id) &
                 ~(Q(date_of_completion__isnull=False) | Q(
                     date_of_cancellation__isnull=False)) &
                 ~Q(status='new'))
            ).order_by('-date_of_application')
            for application in applications:
                application.status_in_rus = get_russian_status(application.status)
                application.matching_result = calculate_matching_between_job_seeker_and_application(user_data,
                                                                                                    application)
                application.distance = haversine_distance(user_data.address.latitude, user_data.address.longitude,
                                                          application.employer.organization.address.latitude,
                                                          application.employer.organization.address.longitude)
                if application.matching_result >= 50 and (
                        application.distance < 60 or user_data.work_location_preference != 'local'):
                    filtered_applications.append(application)
            filtered_applications = sorted(filtered_applications, key=attrgetter('matching_result'), reverse=True)
        applications = filtered_applications
        context['applications'] = applications
    if is_member:
        applications = Application.objects.filter(employer__organization=organization).order_by('-date_of_application')
        for application in applications:
            application.status_in_rus = get_russian_status(application.status)
        context['applications'] = applications
    return render(request, 'general_templates/organization/organization_view.html', context)


def confirmation(request, confirmation_text):
    if request.method == 'POST':
        if 'confirm' in request.POST:
            # Пользователь подтвердил действие
            return True
        elif 'cancel' in request.POST:
            # Пользователь отменил действие
            return False

    context = {
        'confirmation_text': confirmation_text,
    }
    return render(request, 'components/confirmation_form.html', context)
