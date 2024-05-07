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
from domain.views.employers_views.general_views import *
from domain.views.general_views.general_views import *
from domain.views.employee_views.job_seeker_views import *
from domain.views.job_seeker_views.general_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('eme/', include([
        path('applications/', include([
            path('', applications_view, name='applications_view'),
            path('<str:ordering>', applications_view, name='applications_view'),
            path('detail/<str:application_id>', application_detail_view, name='applications_view_detail'),
        ])),

        path('interview/', include([
            path('invite/<str:application_response_id>', invite_job_seeker_on_interview,
                 name='invite_job_seeker_on_interview'),
            path('feedback/<str:interview_id>', create_interview_feedback, name='create_interview_feedback'),
            path('', employee_interviews_view, name='employee_interviews_view'),
            path('<int:archive>', employee_interviews_view, name='employee_interviews_view'),
        ])),

        path('jobseeker/', include([
            path('view', job_seeker_all_view, name='job_seeker_list'),
            path('<str:job_seeker_id>', job_seeker_view, name='job_seeker_view'),
            path('document/', include([
                path('view/<str:document_confirmation_id>', document_required_in_confirmation_view, name='document_required_in_confirmation_view'),
            ])),
        ])),

        path('responce/reject/<str:application_response_id>', reject_job_seeker_response,
             name='reject_job_seeker_response'),

        path('references/', include([
            path('', references_view, name='references'),
            path('<str:reference>', references_view, name='references'),
        ])),

        path('reports/', include([
            path('', select_report_view, name='select_report_view'),
            path('applications_report', applications_report, name='applications_report'),
        ])),
    ])),

    path('js/', include([
        path('profile/', include([
            path('skills', skills_view, name='job_seeker_skills'),
            path('specializations', specialization_view, name='job_seeker_specializations'),
            path('software_and_hardware_tools', software_and_hardware_tools_view,
                 name='job_seeker_software_and_hardware_tools'),
            path('education/', include([
                path('add', job_seeker_education_view, name='job_seeker_education'),
                path('delete/<int:education_id>', delete_education_view, name='delete_education'),
            ])),
            path('work_experience/', include([
                path('add', job_seeker_work_experience_view, name='job_seeker_work_experience'),
                path('delete/<int:work_experience_id>', delete_work_experience_view, name='delete_work_experience_view'),
            ])),
        ])),
        path('application/', include([
            path('view/<str:application_id>', job_seeker_application_view, name='job_seeker_application_view'),
            path('response/', include([
                path('all/', include([
                    path('', job_seeker_application_responses_all_view,
                         name='job_seeker_application_responses_all_view'),
                    path('archive', job_seeker_application_responses_all_archive_view,
                         name='job_seeker_application_responses_all_archive_view'),
                ])),
                path('<str:application_id>/', job_seeker_application_response_create,
                     name='job_seeker_application_response_create'),
                path('<str:application_id>/withdraw', job_seeker_application_response_withdraw,
                     name='job_seeker_application_response_withdraw'),
            ])),
            path('interview/', include([
                path('all/', include([
                    path('', job_seeker_interviews_view, name='job_seeker_interviews_view'),
                    path('<int:archive>', job_seeker_interviews_view, name='job_seeker_interviews_view'),
                ])),
                path('accept/<str:interview_id>', accept_invite_on_interview, name='accept_invite_on_interview'),
                path('reject/<str:interview_id>', reject_invite_on_interview, name='reject_invite_on_interview'),
            ])),
        ]))
    ])),

    path('emr/', include([
        path('profile/', include([
            path('edit/', include([
                path('organization/', include([
                    path('create/', organization_create_view, name='organization_create'),
                    path('apply/<str:organization_id>', organization_apply_view, name='organization_apply'),
                    path('edit/<str:organization_id>', organization_edit_view, name='organization_edit'),
                    path('untie/', organization_untie_view, name='organization_untie'),
                ]))
            ]))
        ])),
        path('applications/', include([
            path('create', application_create_view, name='application_create'),
            path('apply/<str:application_response_id>', apply_job_seeker, name='apply_job_seeker'),
        ])),
        path('job_seeker/<str:job_seeker_id>', allowed_job_seeker_view, name='allowed_job_seeker_view'),
    ])),

    path('login', v.LoginView.as_view(next_page='home'), name='login'),
    path('logout', v.LogoutView.as_view(next_page='login'), name='logout'),

    path('select_user_type', choose_user_type, name='select_user_type'),
    path('registration/<str:user_type>', registration, name='registration'),

    path('profile/', profile, name='user_profile'),
    path('profile/edit', profile_update, name='profile_update'),

    path('organization/<str:organization_id>', organization_view, name='organization_view'),

    path('error_page/<str:error_message>', error_view, name='error_page'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
