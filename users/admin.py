from statistics import mode

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, OauthInfo, PersonalInfo, UserMedia


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
                    "is_phone_verified",
                    "is_email_verified",
                    "can_trade",
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
    """
    This class is used to register the PersonalInfo model to the admin panel.
    """

    model = PersonalInfo
    list_display = ("id", "user", "first_name", "last_name", "created_at")
    list_filter = ()


@admin.register(OauthInfo)
class OautInfoAdmin(admin.ModelAdmin):
    """
    This class is used to register the OauthInfo model to the admin panel.
    """

    model = OauthInfo
    list_display = ("id", "user", "secret", "is_enabled", "created_at")
    list_filter = ("user",)
    search_fields = (
        "id",
        "user",
    )


@admin.register(UserMedia)
class UserMediaAdmin(admin.ModelAdmin):
    """
    This class is used to register the OauthInfo model to the admin panel.
    """

    model = OauthInfo
    list_display = ("id", "user", "created_at")
    list_filter = ("user",)
    search_fields = (
        "id",
        "user",
    )
