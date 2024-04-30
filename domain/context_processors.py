from django.contrib.auth.context_processors import auth

import Hephaestus
from domain.models import JobSeeker, Employer, Employee


def get_user_type(user_id):
    try:
        job_seeker = JobSeeker.objects.get(id=user_id)
        return 'job_seeker'
    except JobSeeker.DoesNotExist:
        pass

    try:
        employer = Employer.objects.get(id=user_id)
        return 'employer'
    except Employer.DoesNotExist:
        pass

    try:
        employee = Employee.objects.get(id=user_id)
        return 'employee'
    except Employee.DoesNotExist:
        return None


def user(request):
    user_id = request.user.id
    user_type = get_user_type(user_id)
    return {'user': request.user, 'user_type': user_type, 'DADATA_API_KEY': Hephaestus.settings.DADATA_API_KEY}