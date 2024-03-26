from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from domain.decorators import *
from domain.forms.general_forms import *
from domain.forms.job_seekers_forms import JobSeekerForm
from domain.models import *


# Create your views here.


def home_view(request, *args, **kwargs):
    applications_by_new = Application.objects.all().order_by('-date_of_application').exclude(
        Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))[:5]
    applications_by_final_date = Application.objects.all().order_by('final_date').exclude(
        Q(date_of_completion__isnull=False) | Q(date_of_cancellation__isnull=False))[:5]
    response = {
        'applications_by_new': applications_by_new,
        'applications_by_final_date': applications_by_final_date
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


def get_user_type(user_id):
    try:
        job_seeker = JobSeeker.objects.get(id=user_id)
        user_type = 'job_seeker'
    except JobSeeker.DoesNotExist:
        try:
            employer = Employer.objects.get(id=user_id)
            user_type = 'employer'
        except Employer.DoesNotExist:
            try:
                employee = Employee.objects.get(id=user_id)
                user_type = 'employee'
            except Employee.DoesNotExist:
                return None, 'not_found'
    return user_type


def get_user_data(user_id):
    user_type = get_user_type(user_id)
    if user_type == 'job_seeker':
        try:
            return JobSeeker.objects.get(id=user_id)
        except JobSeeker.DoesNotExist:
            return None
    elif user_type == 'employer':
        try:
            return Employer.objects.get(id=user_id)
        except Employer.DoesNotExist:
            return None
    elif user_type == 'employee':
        try:
            return Employee.objects.get(id=user_id)
        except Employee.DoesNotExist:
            return None
    else:
        return None


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
    context = {'user': user,
               'data': data,
               'user_type': user_type,
               'form': form}
    return render(request, 'general_templates/profile/update_profile.html', context)