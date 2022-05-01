import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

coin_types = (("notset", "notset"), ("crypto", "crypto"), ("fiat-irt", "fiat-irt"))

COIN_STATUS = (
    ("enable", "enable"),
    ("disable", "disable"),
)


PAID_STATUS = (
    ("pending", "pending"),
    ("paid", "paid"),
    ("faild", "faild"),
    ("expired", "expired"),
)


class StatusModel(models.Model):
    """
    Abstract class to implement coin status attributes
    """

    status = models.CharField(
        "وضعیت", max_length=20, choices=COIN_STATUS, default="disable"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Coin(StatusModel):
    """
    Coins Model
    """

    coin = models.CharField(verbose_name="Coin Name", max_length=50, unique=True)
    symbol = models.CharField(
        verbose_name="Symbol Coin name", max_length=50, unique=True
    )
    lowprice = models.FloatField()
    highprice = models.FloatField()
    cointype = models.CharField(
        verbose_name="Coin Type", max_length=50, choices=coin_types, default="notset"
    )

    def __str__(self):
        return f"{self.coin}"


class UserWallet(models.Model):
    """
    User Wallet
    """

    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="uwallet")
    coin = models.ForeignKey(to=Coin, on_delete=models.PROTECT)
    balance = models.FloatField(verbose_name="Balance", default=0)
    update_time = models.DateTimeField(
        verbose_name="Update Time", editable=True, auto_now_add=True
    )

    def __str__(self):
        return f"{self.user}-{self.coin}"


class Transaction(StatusModel):

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    coin_pairs = models.CharField(verbose_name="Coin pairs", max_length=50)
    coin_out = models.ForeignKey(
        to=UserWallet, on_delete=models.CASCADE, related_name="tcoinout"
    )
    coin_in = models.ForeignKey(
        to=UserWallet, on_delete=models.CASCADE, related_name="tcoinin"
    )
    amount = models.FloatField()
    get_amount = models.FloatField()
    status = models.CharField(
        "وضعیت", max_length=20, choices=PAID_STATUS, default="disable"
    )

    def __str__(self):
        return f"{self.user}-{self.coin_pairs}"
