from django.http import HttpResponse
from django.shortcuts import render, redirect
from domain.models import *
# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, 'home/home.html')


def error_view(request, error_message):
    return render(request, 'components/error.html', {'error_message': error_message})


def references_view(request, reference='OrganizationalLegalForm'):
    references_dict = {
        'OrganizationalLegalForm': [OrganizationalLegalForm, 'Организационно-правовые формы'],
        'Skill': [Skill, 'Навыки'],
        'Specialization': [Specialization, 'Специализации'],
        'SoftwareAndHardwareTool': [SoftwareAndHardwareTool, 'Программно-технические средства'],
        'WorkSchedule': [WorkSchedule, 'Графики работы'],
    }

    if reference in references_dict:
        selected_model = references_dict[reference][0]
        display_model = selected_model.objects.all()
        display_name = selected_model._meta.verbose_name_plural
        fields_names = [field for field in selected_model._meta.get_fields() if not field.is_relation and field.name != 'id']

        response = {
            'model': display_model,
            'display_name': display_name,
            'fields_names': fields_names,
            'references_dict': references_dict
        }

        return render(request, 'references/references.html', response)
    else:
        # Редирект на страницу ошибки с параметром
        error_message = f"Справочник {reference} не найден"
        return redirect('error_page', error_message=error_message)
