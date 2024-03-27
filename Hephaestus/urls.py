"""
URL configuration for Hephaestus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as v
from domain.views.employee_views.employres_views import *
from domain.views.employee_views.general_views import *
from domain.views.general_views.general_views import *
from domain.views.employee_views.job_seeker_views import *
from domain.views.job_seeker_views.general_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('emp/', include([
        path('applications/', applications_view, name='applications_view'),
        path('applications/detail/<str:application_id>', application_detail_view, name='applications_view_detail'),
        path('applications/detail/<str:application_id>/filter/', job_seeker_filter_for_application,
             name='applications_responses_create'),
        path('applications//detail/<str:application_id>/add/<str:job_seeker_id>', add_job_seeker_for_application,
             name='add_job_seeker_for_application'),
        path('applications/<str:ordering>', applications_view, name='applications_view'),
        path('applications/create/organization/', organization_create_view, name='organization_create'),
        path('applications/create/organization/<str:organization_id>/employer/', employers_create_view,
             name='employers_create'),
        path('applications/create/employer/<str:employer_id>', application_create_view, name='application_create'),
        path('jobseeker/view/', job_seeker_all_view, name='job_seeker_list'),
        path('jobseeker/<str:job_seeker_id>', job_seeker_view, name='job_seeker_view'),

        path('references/', references_view, name='references'),
        path('references/<str:reference>/', references_view, name='references'),
    ])),
    path('js/', include([
        path('profile/', include([
            path('skills/', skills_view, name='job_seeker_skills'),
            path('specializations/', specialization_view, name='job_seeker_specializations'),
            path('software_and_hardware_tools/', software_and_hardware_tools_view,
                 name='job_seeker_software_and_hardware_tools'),
            path('education/', job_seeker_education_view, name='job_seeker_education'),
            path('work_experience/', job_seeker_work_experience_view,
                 name='job_seeker_work_experience'),
        ])),
    ])),
    path('login/', v.LoginView.as_view(next_page='home'), name='login'),
    path('select_user_type/', choose_user_type, name='select_user_type'),
    path('employer-registration/', employer_registration, name='employer_registration'),
    path('jobseeker-registration/', jobseeker_registration, name='jobseeker_registration'),
    path('logout/', v.LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', profile, name='user_profile'),
    path('profile/edit/', profile_update, name='profile_update'),

    path('error_page/<str:error_message>/', error_view, name='error_page'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
