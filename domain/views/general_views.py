from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
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
        'EducationLevel': [EducationLevel, 'Уровень образования'],
        'Position': [Position, 'Должность'],
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
