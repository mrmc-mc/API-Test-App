from django.contrib.auth import get_user_model
from django.db.models import F, Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Coin, Transaction, UserWallet
from .utils import SplitPairs

User = get_user_model()


class TransactionSerializer(serializers.ModelSerializer):

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.user = self.context['request'].user.id

    # user = serializers.PrimaryKeyRelatedField(read_only=True)
    coin_pairs = serializers.CharField(required=True)
    # coin_out = serializers.RelatedField(read_only=True)
    # coin_in = serializers.RelatedField(read_only=True)
    get_amount = serializers.FloatField()
    amount = serializers.FloatField()
    # coin_in = serializers.SerializerMethodField(read_only=True)
    # coin_out = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ["amount", "coin_pairs", "coin_in",
                  "coin_out", "user", "get_amount"]
        extra_kwargs = {
            'user': {'write_only': True},
            'coin_out': {'write_only': True},
            'coin_in': {'write_only': True},
        }

    def to_internal_value(self, data):
        __coinin = self.context['request'].user.uwallet.get(coin__symbol=SplitPairs(data['coin_pairs'])[0])
        __coinout = self.context['request'].user.uwallet.get(coin__symbol=SplitPairs(data['coin_pairs'])[1])
        data['coin_in'] = (__coinin).uid
        data['coin_out'] = (__coinout).uid
        data['user'] = self.context['request'].user.id
        data['get_amount'] = ((__coinout.coin.lowprice * float(data['amount'])) / __coinin.coin.highprice)
        return super().to_internal_value(data)

    def validate_coin_pairs(self, attrs):

        if not SplitPairs(attrs):
            raise serializers.ValidationError(
                {"coin_pairs": "incorrect coin pairs!."})

        _coinin, _coinout = SplitPairs(attrs)

        if (Coin.objects.values_list('coin', flat=True).filter(
                Q(symbol=_coinin) | Q(symbol=_coinout)).count()) != 2:
            raise serializers.ValidationError(
                {"coin": "incorrect coin!."})

        # Can use one query(this is sample use)
        # query for get uid for coin_in and coin_out
        
        # _coin_in = UserWallet.objects.get(
        #     coin__symbol=_coinin)

        # _coin_out = UserWallet.objects.get(
        #     coin__symbol=_coinout)
        # self.initial_data['coin_in'] = _coin_in.uid
        # self.context["request"].jwt_data['coin_out'] = _coin_out.uid
        # self.context["request"].jwt_data['get_amount'] = ((_coin_out.coin.lowprice *
        #                                                    self.context["request"].jwt_data['amount']) /
        #                                                   _coin_in.coin.highprice)

        return attrs

    def validate_coin_out(self, attrs):
        print(f"validate====================================")
        if attrs.balance < 5:
            raise serializers.ValidationError(
                {"balance": "Insufficient Balance!"})

        return attrs

    # a function for ad get_amount to initial_data dict
    # def get_initial_data(self):


    def validate_amount(self, attrs):
        if attrs < 5:
            raise serializers.ValidationError(
                {"amount": "Amount Lower than minimum amount!"})

        return attrs


    def create(self, validated_data):
        # coin_in = validated_data['coin_in']
        # coin_out = validated_data['coin_out']
        # _get_amount = ((self.coin_out.lowprice *
        #                validated_data['amount']) /
        #                self.coin_in.highprice)
        # self.context["request"].jwt_data['get_amount'] = _get_amount

        # user.uwallet.get(coin=self.coin_in).update(
        #     balance=F("balance")+_get_amount)
        # user.uwallet.get(coin=self.coin_out).update(
        #     balance=F("balance")+validated_data['amount'])

        return super().create(validated_data)
