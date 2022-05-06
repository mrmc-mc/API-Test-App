from symtable import Symbol
from django.contrib.auth import get_user_model
from django.db import close_old_connections
from django.db.models import F
from rest_framework import serializers
# from rest_framework.validators import UniqueValidator

import coins

from .models import Transaction, UserWallet, Coin
from .utils import SplitPairs

User = get_user_model()


class TransactionSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the Transaction model. validate data and create a new transaction.
    """

    coin_pairs = serializers.CharField(required=True)
    get_amount = serializers.FloatField()
    amount = serializers.FloatField(required=True)

    class Meta:
        model = Transaction
        fields = ["amount", "coin_pairs", "coin_in", "coin_out", "user", "get_amount"]
        extra_kwargs = {
            "user": {"write_only": True},
            "coin_out": {"write_only": True},
            "coin_in": {"write_only": True},
        }

    def to_internal_value(self, data):
        __coinin = self.context["request"].user.uwallet.get(
            coin__symbol=SplitPairs(data["coin_pairs"])[0]
        )
        __coinout = self.context["request"].user.uwallet.get(
            coin__symbol=SplitPairs(data["coin_pairs"])[1]
        )
        data["coin_in"] = (__coinin).uid or None
        data["coin_out"] = (__coinout).uid or None
        data["user"] = self.context["request"].user.id
        data["get_amount"] = (
            (__coinout.coin.lowprice * float(data["amount"])) / __coinin.coin.highprice
        ) or None

        return super().to_internal_value(data)

    def validate_coin_pairs(self, attrs):

        if not SplitPairs(attrs):
            raise serializers.ValidationError({"coin_pairs": "incorrect coin pairs!."})

        if SplitPairs(attrs)[0] == SplitPairs(attrs)[1]:
            raise serializers.ValidationError(
                {"coin_pairs": "incorrect coin pairs(same coins)!."}
            )

        return attrs

    def validate_coin_in(self, attrs):

        if not attrs:
            raise serializers.ValidationError({"coin_in": "incorrect coin to buy!"})

        return attrs

    def validate_coin_out(self, attrs):
        if not attrs:
            raise serializers.ValidationError({"coin_out": "incorrect coin to sell!"})

        return attrs

    def validate_amount(self, attrs):
        if attrs < 5:
            raise serializers.ValidationError(
                {"amount": "Amount Lower than minimum amount!"}
            )

        if (
            attrs
            > self.context["request"]
            .user.uwallet.get(uid=self.initial_data["coin_out"])
            .balance
        ):
            raise serializers.ValidationError({"amount": "Amount Higher than balance!"})

        return attrs

    def create(self, validated_data):
        try:
            (validated_data["coin_in"]).balance = (
                F("balance") + validated_data["get_amount"]
            )
            (validated_data["coin_in"]).save()

            (validated_data["coin_out"]).balance = (
                F("balance") - validated_data["amount"]
            )
            (validated_data["coin_out"]).save()

            validated_data["status"] = "paid"
        except Exception:
            raise serializers.ValidationError(
                {"error": "Something went wrong! Cant create Transaction"}
            )

        finally:
            close_old_connections()

        return super().create(validated_data)



class CoinSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the Coin model.
    """

    class Meta:
        model = Coin
        fields = ["coin", "symbol", "lowprice", "highprice"]




class UserWalletSerializer(serializers.ModelSerializer):
    """
    This is a serializer for the UserWallet model.
    """
    # coin = CoinSerializer(read_only=True)
    coin = serializers.PrimaryKeyRelatedField(read_only=True, source="coin.coin")
    symbol = serializers.PrimaryKeyRelatedField(read_only=True, source="coin.symbol")
        
    class Meta:
        model = UserWallet
        fields = (
            # "user",
            "coin",
            'symbol',
            "balance",
        )
        extra_kwargs = {
            # "user": {"read_only": True},
            "coin": {'read_only': True},
            "balance": {"read_only": True},
            "symbol": {"read_only": True},
        }
        