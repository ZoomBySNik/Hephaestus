from datetime import timedelta
from datetime import datetime as dt
from django import forms
from django.shortcuts import redirect, render
from domain.forms.employers_forms import *
from domain.models import *


def employers_create_view(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST, request.FILES)
        if form.is_valid():
            employer = form.save()
            return redirect('organization_create', employer_id=employer.id)
    else:
        form = EmployerForm()
    employers = Employer.objects.order_by('surname')
    context = {
        'form': form,
        'employers': employers,
    }
    return render(request, 'employers/create/employers_create.html', context)


def organization_create_view(request, employer_id, organization_id=None):
    organizations_list = Organization.objects.order_by('name')
    employer = Employer.objects.get(id=employer_id)
    if organization_id:
        employer.organization = Organization.objects.get(id=organization_id)
        employer.save()
        return redirect('organization_create', employer.id)
    if employer.organization and employer.position:
        return redirect('application_create', employer_id)
    elif (not employer.position) and employer.organization:
        form_type = 'position'
        if request.method == 'POST':
            form = PositionForm(request.POST)
            if form.is_valid():
                employer.position = form.cleaned_data['position']
                employer.save()
                return redirect('application_create', employer_id)
        else:
            form = PositionForm()
    else:
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

                employer.organization = organization
                employer.position = form.cleaned_data['position']
                employer.save()

                return redirect('application_create', employer_id)
        else:
            form = OrganizationForm()
    context = {
        'form_type': form_type,
        'form': form,
        'employer': employer,
        'organizations': organizations_list
    }
    return render(request, 'employers/create/organization_create.html', context)


def application_create_view(request, employer_id):
    employer = Employer.objects.get(id=employer_id)
    employee = Employee.objects.get(id=request.user.id)
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
        applications = Application.objects.exclude(status__in=archive_statuses)
    elif ordering in ordering_mas_archive:
        applications = Application.objects.filter(status__in=archive_statuses)
    if ordering == ordering_mas[0] or ordering == ordering_mas_archive[0]:
        applications = Application.objects.order_by('-date_of_application')
    elif ordering == ordering_mas[1] or ordering == ordering_mas_archive[1]:
        applications = Application.objects.order_by('final_date')
    elif ordering == ordering_mas[2] or ordering == ordering_mas_archive[2]:
        applications = Application.objects.select_related('customer').order_by('customer__last_name')
    else:
        applications = Application.objects.order_by('-date_of_application')
    for application in applications:
        application.status_in_rus = get_russian_status(application.status)
    context = {
        'applications': applications,
    }
    return render(request, 'employers/view/applications_view.html', context)