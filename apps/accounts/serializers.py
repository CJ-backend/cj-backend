from rest_framework import serializers

from .models import Account, TransactionHistory, recalculate_balances


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
            "is_canceled",
        )
        read_only_fields = (
            "transaction_id",
            "account",
            "balance",
            "transaction_timestamp",
            "is_canceled",
        )
        # 생성 시 필수요청 필드만 따로 지정
        extra_kwargs = {
            "transaction_amount": {"required": True},
            "description": {"required": True},
            "transaction_details": {"required": True},
            "transaction_type": {"required": True},
            "transaction_method": {"required": True},
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

    def update(self, instance, validated_data):
        old_amount = instance.transaction_amount
        new_amount = validated_data.get("transaction_amount", old_amount)
        transaction_type = instance.transaction_type  # 'IN' 또는 'OUT'

        # balance 업데이트
        account = instance.account
        delta = new_amount - old_amount

        if transaction_type == TransactionHistory.IN:
            account.balance += delta
        else:
            account.balance -= delta

        account.save()

        # 실제 필드 업데이트
        instance = super().update(instance, validated_data)

        # 전체 거래 잔액 재계산
        recalculate_balances(account)

        return instance
