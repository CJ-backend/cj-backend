from rest_framework import serializers
from .models import Account, TransactionHistory


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "account_id",
            "account_number",
            "bank_code",
            "account_type",
            "balance",
            "create_at",
            "update_at",
        ]
        read_only_fields = [
            "account_id",
            "balance",
            "create_at",
            "update_at",
        ]
        extra_kwargs = {
            "account_number": {"required": True},
            "bank_code": {"required": True},
            "account_type": {"required": True},
        }

# 거래 생성 전용 Serializer
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = (
            "transaction_id",
            "account",
            "transaction_amount",
            "balance",
            "description",
            "transaction_details",
            "transaction_type",
            "transaction_method",
            "transaction_timestamp",
        )
        read_only_fields = (
            "transaction_id",
            "account",
            "balance",
            "transaction_timestamp",
        )
        # 생성 시 필수요청 필드만 따로 지정
        extra_kwargs = {
            "transaction_amount":   {"required": True},
            "description":          {"required": True},
            "transaction_details":  {"required": True},
            "transaction_type":     {"required": True},
            "transaction_method":   {"required": True},
        }

# PATCH
class TransactionPatchSerializer(serializers.ModelSerializer):
   class Meta:
       model = TransactionHistory
       fields = TransactionSerializer.Meta.fields
       read_only_fields = TransactionSerializer.Meta.read_only_fields
       extra_kwargs = {
           f: {"required": False}
           for f in TransactionSerializer.Meta.fields
           if f not in TransactionSerializer.Meta.read_only_fields
       }