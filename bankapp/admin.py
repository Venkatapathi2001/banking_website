from django.contrib import admin
from .models import Account, reg_details, User, Transaction
from django.contrib.auth.admin import UserAdmin

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'balance')

@admin.register(reg_details)
class reg_detailsAdmin(admin.ModelAdmin):
    list_display = ('username', 'firstname', 'lastname', 'email')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'date', 'account')

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'account_number', 'balance', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('account_number', 'balance')}),
    )
