from rest_framework import serializers
from .models import Account
from .models import TransactionHistory


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['account_id', 'user', 'account_number', 'bank_code', 'account_type', 'balance', 'create_at', 'update_at']

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['transaction_type', 'transaction_amount', 'description', 'transaction_details']
