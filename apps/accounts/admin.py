from django.contrib import admin

from .models import Account, TransactionHistory


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ("account_id", "user", "bank_code", "account_number", "balance")
    list_filter = ("bank_code", "account_type")
    search_fields = ("account_number",)


@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_id",
        "account",
        "transaction_amount",
        "balance",
        "description",
        "transaction_type",
        "transaction_method",
        "transaction_timestamp",
    )
    list_filter = (
        "transaction_type",
        "transaction_method",
    )
    search_fields = (
        "description",
        "transaction_details",
    )
