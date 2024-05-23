from django.contrib.auth.context_processors import auth

import Hephaestus
from domain.general_functions import *
from domain.models import JobSeeker, Employer, Employee


def user(request):
    user_id = request.user.id
    user_type = get_user_type(user_id)
    if user_type == 'employee':
        rus_user_type = Employee.objects.get(id=user_id).employee_position.name
    else:
        rus_user_type = get_rus_user_type(user_type)
    return {'user': request.user,
            'user_type': user_type,
            'rus_user_type': rus_user_type,
            'DADATA_API_KEY': Hephaestus.settings.DADATA_API_KEY}
