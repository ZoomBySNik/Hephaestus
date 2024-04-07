import datetime
from domain.models import JobSeeker, Employer, Employee, Application


def calculate_matching_between_job_seeker_and_application(job_seeker, application):
    educations = job_seeker.educationofjobseeker_set.all()
    education_factor = 0
    for education in educations:
        if education.education.education_level.code >= application.education_level.code:
            education_factor = 1
    specializations = job_seeker.specialization.all()
    specialization_factor = 0
    for specialization in specializations:
        if specialization == application.specialization:
            specialization_factor = 1

    work_experiences = job_seeker.workexperience_set.all()
    work_experiences_years = 0
    for work_experience in work_experiences:
        date_of_employment = work_experience.date_of_employment
        date_of_dismissal = work_experience.date_of_dismissal
        if date_of_dismissal == None:
            date_of_dismissal = datetime.datetime.today()
        years_worked = date_of_dismissal.year - date_of_employment.year
        if work_experience.position == application.position:
            work_experiences_years += years_worked
        else:
            work_experiences_years += years_worked * 0.2
    work_experiences_years = work_experiences_years
    if work_experiences_years >= application.experience:
        experience_factor = 1
    else:
        experience_factor = work_experiences_years / application.experience

    skills = job_seeker.skill.all()
    count_of_skills = len(application.skills.all())
    if count_of_skills == 0:
        skill_factor = 1
    else:
        skill_factor = 0
        for skill in skills:
            if skill in application.skills.all():
                skill_factor += 1
        skill_factor = skill_factor / count_of_skills

    software_and_hardware_tools = job_seeker.softwareandhardwaretoolofjobseeker_set.all()
    count_of_software_and_hardware_tools = len(application.software_and_hardware_tools.all())
    if count_of_software_and_hardware_tools == 0:
        software_and_hardware_tool_factor = 1
    else:
        software_and_hardware_tool_factor = 0
        for software_and_hardware_tool in software_and_hardware_tools:
            if software_and_hardware_tool.software_and_hardware_tool in application.software_and_hardware_tools.all():
                software_and_hardware_tool_factor += 1
        software_and_hardware_tool_factor = software_and_hardware_tool_factor / count_of_software_and_hardware_tools

    percent = education_factor * specialization_factor * experience_factor * (
                skill_factor + software_and_hardware_tool_factor) / 2 * 100
    percent = round(percent, 0)
    return percent


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


def get_user_data(user_id):
    user_type = get_user_type(user_id)
    if user_type == 'job_seeker':
        try:
            job_seeker = JobSeeker.objects.get(id=user_id)
            job_seeker.work_experiences = job_seeker.workexperience_set.all().order_by('-date_of_employment')
            return job_seeker
        except JobSeeker.DoesNotExist:
            return None
    elif user_type == 'employer':
        try:
            employer = Employer.objects.get(id=user_id)
            employer.applications = Application.objects.filter(employer=employer)
            for application in employer.applications:
                application.status_in_rus = get_russian_status(application.status)
            return employer
        except Employer.DoesNotExist:
            return None
    elif user_type == 'employee':
        try:
            return Employee.objects.get(id=user_id)
        except Employee.DoesNotExist:
            return None
    else:
        return None


def get_russian_status_in_responses(status):
    status_dict = {
        'pending': 'В ожидании',
        'under_review': 'Рассмотрение',
        'accepted': 'Принят',
        'rejected': 'Отклонен',
        'withdrawn': 'Отозван',
    }
    return status_dict.get(status)


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
