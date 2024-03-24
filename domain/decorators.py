from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

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


def employee_required(view_func):
    """
    Декоратор для проверки, является ли пользователь типом 'employee'.
    """

    def _wrapped_view(request, *args, **kwargs):
        user_type = get_user_type(request.user.id)  # Получаем тип пользователя из контекстного процессора
        if user_type != 'employee':
            return redirect('error_page', error_message='Доступ запрещен')  # Перенаправляем на страницу с ошибкой
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def job_seeker_required(view_func):
    """
    Декоратор для проверки, является ли пользователь типом 'job_seeker'.
    """

    def _wrapped_view(request, *args, **kwargs):
        user_type = get_user_type(request.user.id)  # Получаем тип пользователя из контекстного процессора
        if user_type != 'job_seeker':
            return redirect('error_page', error_message='Доступ запрещен')  # Перенаправляем на страницу с ошибкой
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def employer_required(view_func):
    """
    Декоратор для проверки, является ли пользователь типом 'employer'.
    """

    def _wrapped_view(request, *args, **kwargs):
        user_type = get_user_type(request.user.id)  # Получаем тип пользователя из контекстного процессора
        if user_type != 'employer':
            return redirect('error_page', error_message='Доступ запрещен')  # Перенаправляем на страницу с ошибкой
        return view_func(request, *args, **kwargs)

    return _wrapped_view
