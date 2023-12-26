from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from domain.forms import *
from domain.models import *


# Create your views here.


def home_view(request, *args, **kwargs):
    applications_by_new = Application.objects.all().order_by('-date_of_application')[:5]
    applications_by_final_date = Application.objects.all().order_by('final_date')[:5]
    response = {
        'applications_by_new': applications_by_new,
        'applications_by_final_date': applications_by_final_date
    }
    return render(request, 'home/home.html', response)


def error_view(request, *args):
    return render(request, 'components/error.html', {'error_message': args})


def references_view(request, reference='OrganizationalLegalForm'):
    references_dict = {
        'OrganizationalLegalForm': [OrganizationalLegalForm, 'Организационно-правовые формы'],
        'Skill': [Skill, 'Навыки'],
        'Specialization': [Specialization, 'Специализации'],
        'SoftwareAndHardwareTool': [SoftwareAndHardwareTool, 'Программно-технические средства'],
        'WorkSchedule': [WorkSchedule, 'Графики работы'],
        'EducationLevel': [EducationLevel, 'Уровень образования']
    }

    if reference in references_dict:
        selected_model = references_dict[reference][0]
        display_model = selected_model.objects.all()
        display_name = selected_model._meta.verbose_name_plural
        fields_names = [field for field in selected_model._meta.get_fields() if
                        not field.is_relation and field.name != 'id']
        if request.method == 'POST':
            item_id = request.POST.get('item_id')
            if 'delete_item' in request.POST:
                item = selected_model.objects.get(id=item_id)
                item.delete()
            else:
                print(request.POST.get)
                if item_id:
                    item = selected_model.objects.get(id=item_id)
                else:
                    item = selected_model()
                for field in fields_names:
                    field_name = field.name
                    new_value = request.POST.get(f'{field_name}')
                    setattr(item, field_name, new_value)
                item.save()
        response = {
            'model': display_model,
            'display_name': display_name,
            'fields_names': fields_names,
            'references_dict': references_dict,
            'reference': reference
        }

        return render(request, 'references/references.html', response)
    else:
        error_message = f"Справочник {reference} не найден"
        error_page_url = reverse('error_page', kwargs={'error_message': error_message})
        return redirect(error_page_url)


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
    return render(request, 'employers/employers_create.html', context)


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
    return render(request, 'employers/organization_create.html', context)


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
    return render(request, 'employers/application_create.html', context)


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
        applications = Application.objects.order_by('-final_date')
    elif ordering == ordering_mas[2] or ordering == ordering_mas_archive[2]:
        applications = Application.objects.select_related('customer').order_by('customer__last_name')
    else:
        applications = Application.objects.order_by('-date_of_application')
    for application in applications:
        application.status_in_rus = get_russian_status(application.status)
    context = {
        'applications': applications,
    }
    return render(request, 'employers/applications_view.html', context)
