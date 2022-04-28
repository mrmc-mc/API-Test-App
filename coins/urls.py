from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TradeAPIView

router = DefaultRouter()
router.register(r'trade', TradeAPIView, basename="trade")

app_name = 'coins'

urlpatterns = [
    path("", include("router.urls")),

]
