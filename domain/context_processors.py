from django.contrib.auth.context_processors import auth

from domain.models import JobSeeker, Employer, Employee


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


def user(request):
    return {'user': auth(request)['user'],
            'user_type': get_user_type(auth(request)['user'].id)}
