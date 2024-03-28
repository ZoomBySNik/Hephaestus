import datetime
from domain.decorators import *
from django.db.models import Q
from django.shortcuts import redirect, render
from domain.forms.employers_forms import *
from domain.models import *


@employer_required
def organization_create_view(request, *args, **kwargs):
    organizations_list = Organization.objects.order_by('name')
    form_type = 'organization'
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            address_data = {
                'locality': form.cleaned_data['locality'],
                'street': form.cleaned_data['street'],
                'number_of_building': form.cleaned_data['number_of_building'],
                'apartment_number': form.cleaned_data['apartment_number'],
            }
            addresses = Address.objects.filter(**address_data)

            if addresses.exists():
                address = addresses.first()
            else:
                address = Address.objects.create(**address_data)
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
        form = OrganizationForm(request.POST)
        if form.is_valid():
            address_data = {
                'locality': form.cleaned_data['locality'],
                'street': form.cleaned_data['street'],
                'number_of_building': form.cleaned_data['number_of_building'],
                'apartment_number': form.cleaned_data['apartment_number'],
            }
            addresses = Address.objects.filter(**address_data)

            if addresses.exists():
                address = addresses.first()
            else:
                address = Address.objects.create(**address_data)
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
    return render(request, 'employers_templates/organization/organization_apply.html', context)
