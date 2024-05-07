import calendar
from datetime import date

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse
from domain.general_functions import *
from domain.decorators import *
from domain.forms.general_forms import *
from domain.models import *


@employee_required
def references_view(request, reference='OrganizationalLegalForm'):
    references_dict = {
        'OrganizationalLegalForm': [OrganizationalLegalForm, 'Организационно-правовые формы'],
        'Skill': [Skill, 'Навыки'],
        'Specialization': [Specialization, 'Специализации'],
        'SoftwareAndHardwareTool': [SoftwareAndHardwareTool, 'Программно-технические средства'],
        'WorkSchedule': [WorkSchedule, 'Графики работы'],
        'EducationLevel': [EducationLevel, 'Уровень образования'],
        'Position': [Position, 'Должность'],
    }

    if reference in references_dict:
        selected_model = references_dict[reference][0]
        if reference == 'EducationLevel':
            display_model = selected_model.objects.all().order_by('-code')
        else:
            display_model = selected_model.objects.all().order_by('name')
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

        return render(request, 'employees_templates/references/references.html', response)
    else:
        error_message = f"Справочник {reference} не найден"
        error_page_url = reverse('error_page', kwargs={'error_message': error_message})
        return redirect(error_page_url)


@employee_required
def select_report_view(request):
    context = {}
    return render(request, 'employees_templates/reports/select_report.html', context)


@employee_required
def applications_report(request):
    if request.method == 'POST':
        form = ApplicationSettingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date'] or datetime.date.today().replace(day=1)
            end_date = form.cleaned_data['end_date'] or datetime.date.today().replace(
                day=calendar.monthrange(date.today().year, date.today().month)[1])
            statuses = form.cleaned_data['status']
            employer = form.cleaned_data['employer']

            applications = Application.objects.filter(
                Q(date_of_application__range=[start_date, end_date]) &
                Q(status__in=statuses)
            )
            if employer:
                applications = applications.filter(employer=employer)
            for application in applications:
                application.employer.organization.okved_kode_text = get_okved_description(
                    application.employer.organization.okved_kode)
                application.responses = ApplicationsResponses.objects.filter(application=application)
                application.status_in_rus = get_russian_status(application.status)
                application.count_of_interviews = 0
                for response in application.responses:
                    response.interviews = JobInterview.objects.filter(application_response=response)
                    application.count_of_interviews += response.interviews.count()
                    if response.status == 'accepted':
                        application.job_seeker = response.job_seeker

            # Здесь можно выполнить необходимые действия с датами
            context = {
                'start_date': start_date,
                'end_date': end_date,
                'applications': applications
            }
            return render(request, 'employees_templates/reports/applications_report.html', context)
    else:
        # Если метод запроса GET, показываем пустую форму
        form = ApplicationSettingForm()

    return render(request, 'employees_templates/reports/params/application_report_params.html', {'form': form})


@employee_required
def users_report(request):
    if request.method == 'POST':
        form = UsersSettingForm(request.POST)
        if form.is_valid():
            user_types = form.cleaned_data
            all_users = CustomUser.objects.all().order_by('-last_login')
            users = []
            for user in all_users:
                user.user_type = get_user_type(user.id)
                if user.user_type not in user_types:
                    users.append(user)
                user.user_type = get_rus_user_type(get_user_type(user.id))
            context = {
                'users': users
            }
            return render(request, 'employees_templates/reports/users_report.html', context)
    else:
        # Если метод запроса GET, показываем пустую форму
        form = UsersSettingForm()

    return render(request, 'employees_templates/reports/params/users_report_params.html', {'form': form})
