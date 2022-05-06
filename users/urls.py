from django.urls import path

from .views import (
    ChangePasswordAPIView,
    LoginAPIView,
    LogoutAPIView,
    OauthAPIView,
    OtpRegVerificationAPIView,
    RegisterAPIView,
    UserActivityView,
    UserListAPIView,
)

app_name = "users"

urlpatterns = [
    # Auth path
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("changepw/", ChangePasswordAPIView.as_view(), name="change-password"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("email-verify/", OtpRegVerificationAPIView.as_view(), name="email-verify"),
    path("otp/", OauthAPIView.as_view(), name="otp-verify"),
    # path("reset-password/"),
    # Detail path
    path("list/", UserListAPIView.as_view(), name="list"),
    path("list/statistics/", UserActivityView.as_view(), name="statistics"),
]
