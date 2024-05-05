from datetime import timedelta, date
from datetime import datetime as dt
from django import forms
from django.shortcuts import redirect, render, get_object_or_404
from domain.general_functions import *
from domain.decorators import *
from domain.forms.job_seekers_forms import *
from domain.models import *


@job_seeker_required
def skills_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = SkillsForm(request.POST)
        if form.is_valid():
            existing_skills = list(form.cleaned_data['skills'])

            new_skills = form.cleaned_data['new_skills'].split(',')
            print(new_skills)
            skills = existing_skills
            for skill_name in new_skills:
                skill, created = Skill.objects.get_or_create(name=skill_name)
                skills.append(skill)

            job_seeker.skill.set(skills)
            job_seeker.save()
            return redirect('user_profile')
    else:
        form = SkillsForm(initial={'skills': job_seeker.skill.all()})

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/skills_create.html', context)


@job_seeker_required
def specialization_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = SpecializationForm(request.POST)
        if form.is_valid():
            existing_specializations = list(form.cleaned_data['specializations'])

            new_specializations = form.cleaned_data['new_specializations'].split(',')
            print(new_specializations)
            specializations = existing_specializations
            for specializations_name in new_specializations:
                specialization, created = Specialization.objects.get_or_create(name=specializations_name)
                specializations.append(specialization)

            job_seeker.specialization.set(specializations)
            job_seeker.save()
            return redirect('user_profile')
    else:
        form = SpecializationForm(initial={'specializations': job_seeker.specialization.all()})

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/specialization_create.html', context)


@job_seeker_required
def software_and_hardware_tools_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = SoftwareAndHardwareToolForm(request.POST)

        if form.is_valid():
            selected_tools = list(form.cleaned_data['software_and_hardware_tools'])

            new_tools = form.cleaned_data['new_software_and_hardware_tools'].split(',')
            if new_tools:
                for new_tool in new_tools:
                    tool = SoftwareAndHardwareTool.objects.create(name=new_tool)
                    tool.save()
                    selected_tools.append(tool)
            SoftwareAndHardwareToolOfJobSeeker.objects.filter(job_seeker=job_seeker).delete()
            for tool in selected_tools:
                SoftwareAndHardwareToolOfJobSeeker.objects.create(
                    job_seeker=job_seeker,
                    software_and_hardware_tool=tool
                )

            return redirect('user_profile')
    else:
        selected_tools = SoftwareAndHardwareToolOfJobSeeker.objects.filter(job_seeker=job_seeker)

        initial_data = {
            'software_and_hardware_tools': selected_tools.values_list('software_and_hardware_tool', flat=True)}
        form = SoftwareAndHardwareToolForm(initial=initial_data)

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/software_and_hardware_tools_create.html', context)


@job_seeker_required
def job_seeker_education_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = EducationForm(request.POST, request.FILES,)
        if form.is_valid():
            address = get_or_create_address(form.cleaned_data['education_organization_address_locality'],
                                            form.cleaned_data['education_organization_address_street'],
                                            form.cleaned_data['education_organization_address_number_of_building'])

            education_organization = EducationalOrganization(
                address=address,
                name=form.cleaned_data['education_organization_name']
            )
            education_organization.save()

            education = Education.objects.create(
                organization=education_organization,
                name=form.cleaned_data['name'],
                code=form.cleaned_data['code'],
                education_level=form.cleaned_data['education_level']
            )
            education.save()
            document_confirmation = DocumentConfirmation.objects.create(file=form.cleaned_data['document_photo'])
            document_confirmation.save()
            education_job_seeker = EducationOfJobSeeker.objects.create(
                job_seeker=job_seeker,
                education=education,
                year_received=form.cleaned_data['year_received'],
                document_confirmation=document_confirmation
            )
            education_job_seeker.save()
            return redirect('user_profile')
        print(form.errors)
    else:
        form = EducationForm()

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/education_create.html', context)


@job_seeker_required
def job_seeker_work_experience_view(request):
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            work_experience = WorkExperience.objects.create(
                job_seeker=job_seeker,
                organization=form.cleaned_data['organization'],
                position=form.cleaned_data['position'],
                date_of_employment=form.cleaned_data['date_of_employment'],
                date_of_dismissal=form.cleaned_data['date_of_dismissal']
            )
            work_experience.save()
            return redirect('user_profile')
    else:
        form = WorkExperienceForm()

    context = {
        'job_seeker': job_seeker,
        'form': form,
    }
    return render(request, 'job_seekers_templates/profile/create/work_experience.html', context)


@job_seeker_required
def job_seeker_application_view(request, application_id):
    update_old_overdue()
    application = Application.objects.get(id=application_id)
    response_was_created = False
    can_be_withdrawn = False
    existing_response = ApplicationsResponses.objects.filter(application=application,
                                                             job_seeker=JobSeeker.objects.get(
                                                                 id=request.user.id)).exclude(status='withdrawn')
    if existing_response.exists():
        response_was_created = True
        if existing_response.first().status == 'pending':
            can_be_withdrawn = True
    context = {
        'application': application,
        'response_was_created': response_was_created,
        'can_be_withdrawn': can_be_withdrawn
    }
    return render(request, 'job_seekers_templates/application/application_view.html', context)


@job_seeker_required
def job_seeker_application_response_create(request, application_id):
    update_old_overdue()
    application = Application.objects.get(id=application_id)
    job_seeker = JobSeeker.objects.get(id=request.user.id)

    existing_response = ApplicationsResponses.objects.filter(application=application, job_seeker=job_seeker).first()
    if existing_response:
        if existing_response.status == 'withdrawn':
            existing_response.status = 'pending'
            existing_response.save()
        return redirect('job_seeker_application_view', application_id=application_id)
    application_response = ApplicationsResponses.objects.create(
        application=application,
        job_seeker=job_seeker,
        evaluation=calculate_matching_between_job_seeker_and_application(job_seeker, application),
    )
    application = application_response.application
    application.date_of_last_change = datetime.datetime.now()
    application.save()
    application_response.save()
    return redirect('job_seeker_application_view', application_id=application_id)


@job_seeker_required
def job_seeker_application_response_withdraw(request, application_id):
    update_old_overdue()
    application = Application.objects.get(id=application_id)
    job_seeker = JobSeeker.objects.get(id=request.user.id)

    existing_response = ApplicationsResponses.objects.filter(application=application, job_seeker=job_seeker).first()
    if existing_response:
        if existing_response.status == 'pending':
            existing_response.status = 'withdrawn'
            application = existing_response.application
            application.date_of_last_change = datetime.datetime.now()
            application.save()
            existing_response.save()
        return redirect('job_seeker_application_view', application_id=application_id)
    return redirect('job_seeker_application_view', application_id=application_id)


@job_seeker_required
def job_seeker_application_responses_all_view(request):
    update_old_overdue()
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    responses = ApplicationsResponses.objects.filter(job_seeker=job_seeker).exclude(
        status__in=['accepted', 'rejected', 'withdrawn']
    ).order_by('-application__date_of_application')
    for response in responses:
        response.status_in_rus = get_russian_status_in_responses(response.status)
        response.application.status_in_rus = get_russian_status(response.application.status)
    archive = False
    context = {
        'responses': responses,
        'archive': archive
    }
    return render(request, 'job_seekers_templates/responses/responses_all_view.html', context)


@job_seeker_required
def job_seeker_application_responses_all_archive_view(request):
    update_old_overdue()
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    responses = ApplicationsResponses.objects.filter(job_seeker=job_seeker).filter(
        status__in=['accepted', 'rejected', 'withdrawn']
    ).order_by('-application__date_of_application')
    for response in responses:
        response.status_in_rus = get_russian_status_in_responses(response.status)
        response.application.status_in_rus = get_russian_status(response.application.status)
    archive = True
    context = {
        'responses': responses,
        'archive': archive
    }
    return render(request, 'job_seekers_templates/responses/responses_all_view.html', context)


@job_seeker_required
def job_seeker_interviews_view(request, archive=0):
    update_old_overdue()
    if archive == 0:
        archive = False
    elif archive == 1:
        archive = True
    else:
        return redirect(request.META.get('HTTP_REFERER', None))
    job_seeker = JobSeeker.objects.get(id=request.user.id)
    if not archive:
        interviews = JobInterview.objects.all().filter(application_response__job_seeker=job_seeker).exclude(
            status__in=['rejected', 'with_feedback', 'overdue', 'passed']).order_by('-date_of_interview')
    else:
        interviews = JobInterview.objects.all().filter(application_response__job_seeker=job_seeker).exclude(
            status__in=['pending', 'accepted']).order_by('-date_of_interview')
    for interview in interviews:
        interview.status_in_rus = get_russian_status_interview(interview.status)
    context = {
        'interviews': interviews,
        'archive': archive
    }
    return render(request, 'job_seekers_templates/interviews/interviews.html', context)


@job_seeker_required
def reject_invite_on_interview(request, interview_id):
    interview = JobInterview.objects.get(id=interview_id)
    interview.status = 'rejected'
    application = interview.application_response.application
    application.date_of_last_change = datetime.datetime.now()
    application.save()
    interview.save()
    return redirect(request.META.get('HTTP_REFERER', None))


@job_seeker_required
def accept_invite_on_interview(request, interview_id):
    interview = JobInterview.objects.get(id=interview_id)
    interview.status = 'accepted'
    application = interview.application_response.application
    application.date_of_last_change = datetime.datetime.now()
    application.save()
    interview.save()
    return redirect(request.META.get('HTTP_REFERER', None))
