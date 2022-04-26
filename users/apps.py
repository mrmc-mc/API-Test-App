from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save
from django.conf import settings


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(self):
        from .signals import create_group, sendOTP_after_registration, OauthGenerator
        
        post_migrate.connect(create_group, sender=self)
        post_save.connect(sendOTP_after_registration, sender=settings.AUTH_USER_MODEL)
        post_save.connect(OauthGenerator, sender=settings.AUTH_USER_MODEL)