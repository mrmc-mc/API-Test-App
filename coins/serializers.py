from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Coin, Transaction, UserWallet
from .utils import SplitPairs

User = get_user_model()


class TransactionSerializer(serializers.ModelSerializer):

    amount = serializers.FloatField()

    class Meta:
        model = Transaction
        fields = "__all__"
        extra_kwargs = {
            'user': {'write_only': True},
            'coin_out': {'write_only': True},
            'coin_in': {'write_only': True},
        }

    def validate_coins(self, attrs):
        coin_pairs = str(attrs["coin_pairs"])
        if not SplitPairs(coin_pairs):
            raise serializers.ValidationError(
                {"coin_pairs": "incorrect coin pairs!."})

        coinin, coinout = SplitPairs(coin_pairs)

        if not (Coin.objects.values_list('coin', flat=True).filter(
                Q(symbol=coinin) & Q(symbol=coinout)).exists()):
            raise serializers.ValidationError(
                {"coin": "incorrect coin!."})

        attrs['coin_in'] = Coin.objects.get(symbol=coinin)
        attrs['coin_out'] = Coin.objects.get(symbol=coinout)

        return attrs

    def validate_balance(self, attrs):
        user = self.context['request'].user
        if user.uwallet.get(coin=attrs['coin_out']).balance < attrs['amount']:
            raise serializers.ValidationError(
                {"balance": "Insufficient Balance!"})

        return attrs

    def validate_amount(self, attrs):

        if attrs['amount'] < 5:
            raise serializers.ValidationError(
                {"amount": "Amount Lower than minimum amount!"})

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        coin_in = validated_data['coin_in']
        coin_out = validated_data['coin_out']
        _get_amount = ((coin_out.lowprice *
                       validated_data['amount']) /
                       coin_in.highprice)

        validated_data['get_amount'] = _out_amount

        user.uwallet.get(coin=coin_in).update(balance=F("balance")+_get_amount)
        user.uwallet.get(coin=coin_out).update(
            balance=F("balance")+validated_data['amount'])

        return super().create(validated_data)
