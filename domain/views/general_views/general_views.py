from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from domain.decorators import *
from domain.forms.employers_forms import EmployerForm
from domain.forms.general_forms import *
from domain.forms.job_seekers_forms import JobSeekerForm
from domain.models import *
from domain.general_functions import *


@login_required
def home_view(request, *args, **kwargs):
    applications_by_new = Application.objects.all().order_by('-date_of_application').exclude(
        Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))[:5]
    applications_by_final_date = Application.objects.all().order_by('final_date').exclude(
        Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))[:5]
    extra_data = {}
    if get_user_type(request.user.id) == 'job_seeker':
        job_seeker = get_user_data(request.user.id)
        applications = Application.objects.filter(
            ~Q(applicationsresponses__job_seeker_id=job_seeker.id) &
            ~(Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False)) &
            ~Q(status='new')
        )
        filtered_applications = []
        for application in applications:
            application.matching_result = calculate_matching_between_job_seeker_and_application(job_seeker, application)
            if application.matching_result >= 50:
                filtered_applications.append(application)
        extra_data = {
            'applications': filtered_applications,
            'job_seeker': job_seeker}
    response = {
        'applications_by_new': applications_by_new,
        'applications_by_final_date': applications_by_final_date,
        'extra_data': extra_data
    }
    return render(request, 'general_templates/home/home.html', response)


def error_view(request, error_message):
    context = {'error_message': error_message}
    return render(request, 'components/error.html', context)


def choose_user_type(request):
    return render(request, 'registration/select_user_type.html')


def employer_registration(request):
    if request.method == 'POST':
        form = EmployerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Аутентификация пользователя после регистрации
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            # Переход на страницу с ФИО зарегистрированного пользователя
            return redirect('user_profile')  # Замените 'user_profile' на URL вашей страницы профиля
    else:
        form = EmployerRegistrationForm()
    return render(request, 'registration/user_registration.html', {'form': form})


def jobseeker_registration(request):
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Аутентификация пользователя после регистрации
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            # Переход на страницу с ФИО зарегистрированного пользователя
            return redirect('user_profile')  # Замените 'user_profile' на URL вашей страницы профиля
    else:
        form = JobSeekerRegistrationForm()
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
                    address_data = {
                        'locality': form.cleaned_data['locality'],
                        'street': None,
                        'number_of_building': None,
                        'apartment_number': None
                    }
                    addresses = Address.objects.filter(**address_data)

                    if addresses.exists():
                        address = addresses.first()
                    else:
                        address = Address.objects.create(**address_data)
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
