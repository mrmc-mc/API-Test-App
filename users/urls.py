from django.urls import path
from .views import LoginAPIView, RegisterAPIView, LogoutAPIView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='login'),
    path('login/', LoginAPIView.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
]
