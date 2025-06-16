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


# 거래 생성,조회,삭제
class TransactionSerializer(serializers.ModelSerializer):
    # 계좌 UUID 직접 입력받을 수 있게 설정
    account = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all()
    )

    class Meta:
        model = TransactionHistory
        fields = (
            "transaction_id",
            "account",
            "transaction_amount",
            "balance",
            "description",
            "transaction_type",
            "transaction_method",
            "transaction_timestamp",
            "is_canceled",
        )
        read_only_fields = (
            "transaction_id",
            "balance",
            "transaction_timestamp",
            "is_canceled",
        )
        # 생성 시 필수요청 필드만 따로 지정
        extra_kwargs = {
            "account": {"required": True},
            "transaction_amount": {"required": True},
            "description": {"required": True},
            "transaction_type": {"required": True},
            "transaction_method": {"required": True},
        }

    def validate_account(self, value):
        request = self.context.get("request")

        if not value:
            raise serializers.ValidationError("계좌를 선택해주세요.")

        if value.user != request.user:
            raise serializers.ValidationError("본인의 계좌가 아닙니다.")

        return value


