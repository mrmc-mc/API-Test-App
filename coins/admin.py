from django.contrib import admin
from .models import Coin, UserWallet, Transaction


@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('id', 'coin')
    list_filter = ('coin',)
    search_fields = ('id', 'coin',)
    
    
@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ('uid', 'user', 'coin', 'balance')
    list_filter = ('user',)
    search_fields = ('uid', 'user',)
    
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
    list_filter = ('user',)
    search_fields = ('id', 'user',)
