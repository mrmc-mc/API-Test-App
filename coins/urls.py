from django.urls import path

from .views import TradeAPIView


app_name = 'coins'

urlpatterns = [
    path("trade/", TradeAPIView.as_view(), name="trade"),

]
