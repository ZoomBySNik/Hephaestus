import datetime
from datetime import timedelta, date
from domain.decorators import *
from django.db.models import Q
from django.shortcuts import redirect, render
from domain.forms.employers_forms import *
from domain.models import *
from domain.general_functions import *
from domain.views.general_views.general_views import confirmation


@employer_required
def organization_create_view(request, *args, **kwargs):
    organizations_list = Organization.objects.order_by('name')
    form_type = 'organization'
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, )
        if form.is_valid():
            address = get_or_create_address(form.cleaned_data['locality'], form.cleaned_data['street'],
                                            form.cleaned_data['number_of_building'],
                                            form.cleaned_data['apartment_number'])
            organization = form.save(commit=False)
            organization.address = address
            organization.save()
            employer = Employer.objects.get(id=request.user.id)
            employer.organization = organization
            employer.save()
            return redirect('user_profile')
    else:
        form = OrganizationForm()
    context = {
        'form_type': form_type,
        'form': form,
        'organizations': organizations_list
    }
    return render(request, 'employers_templates/organization/organization_apply.html', context)


@employer_required
def organization_apply_view(request, organization_id):
    employer = Employer.objects.get(id=request.user.id)
    employer.organization = Organization.objects.get(id=organization_id)
    employer.save()
    return redirect('user_profile')


@employer_required
def organization_untie_view(request, *args, **kwargs):
    employer = Employer.objects.get(id=request.user.id)
    employer.organization = None
    employer.position = None
    employer.save()
    return redirect('user_profile')


@employer_required
def organization_edit_view(request, organization_id):
    form_type = 'organization'
    organization = Organization.objects.get(id=organization_id)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            address = get_or_create_address(form.cleaned_data['locality'], form.cleaned_data['street'],
                                            form.cleaned_data['number_of_building'],
                                            form.cleaned_data['apartment_number'])
            organization = form.save(commit=False)
            organization.address = address
            organization.save()
            return redirect('user_profile')
    else:
        form = OrganizationForm(instance=organization,
                                initial={'locality': organization.address.locality,
                                         'street': organization.address.street,
                                         'number_of_building': organization.address.number_of_building,
                                         'apartment_number': organization.address.apartment_number})
    context = {
        'form_type': form_type,
        'form': form,
    }
    return render(request, 'employers_templates/organization/organization_edit.html', context)


@employer_required
def application_create_view(request):
    employer = Employer.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            position_data = {
                'name': form.cleaned_data['position'],
            }
            positions = Position.objects.filter(**position_data)
            if positions.exists():
                position = positions.first()
            else:
                position = Position.objects.create(**position_data)
            application = form.save(commit=False)
            application.position = position
            application.employer = employer
            application.date_of_last_change = datetime.datetime.now()
            application.save()
            form.save_m2m()

            return redirect('home')
    else:
        form = ApplicationForm()
    context = {
        'employer': employer,
        'form': form
    }
    return render(request, 'employers_templates/applications/create/application_create.html', context)


@employer_required
def allowed_job_seeker_view(request, job_seeker_id):
    job_seeker = JobSeeker.objects.get(id=job_seeker_id)
    employer = Employer.objects.get(id=request.user.id)
    responses = ApplicationsResponses.objects.filter(
        Q(job_seeker=job_seeker) & Q(application__employer=employer) & Q(status='sent_to_employer'))
    if responses:
        if job_seeker.birthdate:
            job_seeker.age = (date.today() - job_seeker.birthdate) // timedelta(days=365.2425)
        else:
            job_seeker.age = None
        work_experiences = job_seeker.workexperience_set.all().order_by('-date_of_employment')
        context = {
            'job_seeker': job_seeker,
            'work_experiences': work_experiences,
        }
        return render(request, 'employees_templates/job_seekers/view/job_seeker_view.html', context)
    else:
        return redirect(request.META.get('HTTP_REFERER', None))


@employer_required
def apply_job_seeker(request, application_response_id):
    application_response = ApplicationsResponses.objects.get(id=application_response_id)

    if request.method == 'POST':
        if confirmation(request,
                        str('Вы собираетесь принять соискателя ' + application_response.job_seeker.last_name +
                            application_response.job_seeker.first_name +
                            application_response.job_seeker.patronymic + ' и закрыть заявку?')):
            application_response.status = 'accepted'
            application = Application.objects.get(id=application_response.application.id)
            application.status = 'completed'
            application.date_of_completion = datetime.datetime.now()
            another_responses = ApplicationsResponses.objects.filter(application=application)
            application_response.save()
            application.date_of_last_change = datetime.datetime.now()
            application.save()
            for response in another_responses:
                if response.id != application_response.id:
                    response.status = 'rejected'
                    response.description = 'Найден другой кандидат'
                    response.save()
                    interviews = JobInterview.objects.filter(application_response=response)
                    for interview in interviews:
                        if interview.status in ['pending', 'accepted']:
                            interview.status = 'rejected'
                            interview.description = 'Собеседование отменено по причине закрытия заявки'
                            interview.save()
            return redirect('home')
        else:
            return redirect(request.META.get('HTTP_REFERER', None))
    else:
        return confirmation(request,
                            str('Вы собираетесь принять соискателя ' + application_response.job_seeker.last_name +
                                application_response.job_seeker.first_name +
                                application_response.job_seeker.patronymic + ' и закрыть заявку?'))
