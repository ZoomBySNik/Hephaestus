from django.contrib import admin
from django.contrib.auth.hashers import make_password

from domain.models import CustomUser


class CustomInAdminUser(CustomUser):
    ordering = ('id', 'last_login', 'username', 'password', 'last_name', 'first_name', 'patronymic', 'email',
                'phone_number', 'profile_photo', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')

    def save_model(self, request, obj, form, change):
        # Хешируем пароль перед сохранением пользователя
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(CustomInAdminUser)
