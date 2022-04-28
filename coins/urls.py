from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'trade', views.ArticleViewSet)

app_name = 'coins'

urlpatterns = [
    path("", include("router.urls")),

]
