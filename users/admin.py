from statistics import mode
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, OauthInfo, PersonalInfo


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        "email",
        "phone",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "phone",
                    "first_name",
                    "last_name",
                    "national_code",
                    "is_phone_verified",
                    "is_email_verified",
                    "can_trade",
                    "image_file",
                    "ref_code",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    model = PersonalInfo
    list_display = ("id", "user", "first_name", "last_name", "created_at")
    list_filter = ()


@admin.register(OauthInfo)
class OautInfoAdmin(admin.ModelAdmin):
    model = OauthInfo
    list_display = ("id", "user", "secret", "is_enabled", "created_at")
    list_filter = ("user",)
    search_fields = (
        "id",
        "user",
    )
