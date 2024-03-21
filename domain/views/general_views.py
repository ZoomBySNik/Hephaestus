from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from domain.forms.general_forms import *
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
        'EducationLevel': [EducationLevel, 'Уровень образования'],
        'Position': [Position, 'Должность'],
    }

    if reference in references_dict:
        selected_model = references_dict[reference][0]
        if reference == 'EducationLevel':
            display_model = selected_model.objects.all().order_by('-code')
        else:
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
    return render(request, 'profile.html', {'user': user})