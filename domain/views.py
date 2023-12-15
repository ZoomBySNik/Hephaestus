from django.http import HttpResponse
from django.shortcuts import render, redirect
from domain.models import *
# Create your views here.


def home_view(request, *args, **kwargs):
    return render(request, 'home/home.html')


def error_view(request, error_message):
    return render(request, 'components/error.html', {'error_message': error_message})


def references_view(request, reference='OrganizationalLegalForm'):
    models_dict = {
        'OrganizationalLegalForm': OrganizationalLegalForm,
        'Skill': Skill,
        'Specialization': Specialization,
        'SoftwareAndHardwareTool': SoftwareAndHardwareTool,
        'WorkSchedule': WorkSchedule,
        # Добавьте другие модели по мере необходимости
    }

    if reference in models_dict:
        selected_model = models_dict[reference]
        display_model = selected_model.objects.all()
        display_name = selected_model._meta.verbose_name_plural
        fields_names = [field for field in selected_model._meta.get_fields() if not field.is_relation and field.name != 'id']

        response = {
            'model': display_model,
            'display_name': display_name,
            'fields_names': fields_names,
        }

        return render(request, 'references/references.html', response)
    else:
        # Редирект на страницу ошибки с параметром
        error_message = f"Справочник {reference} не найден"
        return redirect('error_page', error_message=error_message)
