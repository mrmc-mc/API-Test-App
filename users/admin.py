from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PersonalInfo


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'phone','is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','phone', 'password',"is_email_verified","is_phone_verified")}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)


# class UserOTPAdmin(admin.ModelAdmin):
#     model = UserOTP
#     list_display = ('id', 'email_otp','mobile_otp','created_at')
#     list_filter = ()


# admin.site.register(UserOTP, UserOTPAdmin)

class PersonalInfoAdmin(admin.ModelAdmin):
    model = PersonalInfo
    list_display = ('id', 'user','first_name', 'last_name', 'created_at')
    list_filter = ()


admin.site.register(PersonalInfo, PersonalInfoAdmin)