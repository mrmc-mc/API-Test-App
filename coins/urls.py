from django.urls import path

from .views import TradeAPIView, UserWalletAPIView


app_name = 'coins'

urlpatterns = [
    path("trade/", TradeAPIView.as_view(), name="trade"),
    path("wallet/", UserWalletAPIView.as_view(), name="wallet"),

]
