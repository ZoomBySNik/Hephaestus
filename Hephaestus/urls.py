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
from django.urls import path
from django.conf.urls.static import static
from django.contrib.auth import views as v
from domain.views.employres_views import *
from domain.views.general_views import *
from domain.views.job_seeker_views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),

    path('employers/create/', employers_create_view, name='employers_create'),
    path('employers/create/<str:employer_id>/organization/', organization_create_view, name='organization_create'),
    path('employers/create/<str:employer_id>/organization/<str:organization_id>', organization_create_view, name='organization_create'),
    path('employers/create/<str:employer_id>/application/', application_create_view, name='application_create'),

    path('applications/', applications_view, name='applications_view'),
    path('applications/<str:ordering>', applications_view, name='applications_view'),

    path('jobseeker/create/', job_seeker_create_view, name='job_seeker_create'),

    path('references/', references_view, name='references'),
    path('references/<str:reference>/', references_view, name='references'),

    path('login/', v.LoginView.as_view(next_page='home'), name='login'),
    path('logout/', v.LogoutView.as_view(next_page='login'), name='logout'),

    path('error_page/<str:error_message>/', error_view, name='error_page'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
