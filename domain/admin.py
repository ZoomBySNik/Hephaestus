from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.apps import apps
from domain.models import CustomUser

# Register your models here.
app_config = apps.get_app_config('domain')


class CustomInAdminUser(CustomUser):
    ordering = ('id', 'last_login', 'username', 'password', 'last_name', 'first_name', 'patronymic', 'email',
                'phone_number', 'profile_photo', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions')

    def save_model(self, request, obj, form, change):
        # Хешируем пароль перед сохранением пользователя
        obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


# Те модели которые не нужно регистрировать!!! Их нужно импортнуть отдельно
NOT_REGISTERED_MODELS = [CustomInAdminUser, CustomUser]
for model in app_config.get_models():
    if not (model in NOT_REGISTERED_MODELS):
        admin.site.register(model)
# Register your models here.
admin.site.register(CustomInAdminUser)
