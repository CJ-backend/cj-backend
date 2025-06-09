import uuid

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

from apps.constants import (ACCOUNT_TYPE, BANK_CODES, TRANSACTION_METHOD,
                            TRANSACTION_TYPE)


# 유저의 계좌 정보를 저장하는 테이블
class Account(models.Model):
    # PK: UUID 자동 생성
    account_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 어느 유저의 계좌인지 (1:N), 유저 삭제 시 계좌도 삭제
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts"
    )
    # 은행 발급 계좌번호, 중복 금지 및 형식 검증
    account_number = models.CharField(
        "Account Number",
        max_length=30,
        unique=True,
        validators=[RegexValidator(r"^\d{10,30}$", "숫자만 입력 (10~30자리)")],
    )
    # constants.py 의 은행 코드 선택지
    bank_code = models.CharField("Bank Code", max_length=10, choices=BANK_CODES)
    # 계좌 종류
    account_type = models.CharField("Account Type", max_length=30, choices=ACCOUNT_TYPE)
    # 잔액 (소수점 2자리)
    balance = models.DecimalField("Balance", max_digits=18, decimal_places=2, default=0)
    create_at = models.DateTimeField("Create At", auto_now_add=True)  # 생성 일시
    update_at = models.DateTimeField("Update At", auto_now=True)  # 수정 일시

    class Meta:
        db_table = "account"
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.email} | {self.bank_code}:{self.account_number}"


# 계좌별 거래 내역을 저장하는 테이블
class TransactionHistory(models.Model):
    # PK: UUID 자동 생성
    transaction_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    # 어떤 계좌의 거래인지 (1:N), 계좌 삭제 시 내역 삭제
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="transactions"
    )
    # 거래 금액
    transaction_amount = models.DecimalField(
        "Transaction Amount", max_digits=18, decimal_places=2
    )
    # 거래 후 잔액
    post_transaction_amount = models.DecimalField(
        "Post Transaction Amount", max_digits=18, decimal_places=2
    )
    # 간단 설명
    description = models.CharField("Description", max_length=255)
    # ATM/계좌이체/카드결제 등 방법 구분
    transaction_details = models.CharField("Transaction Details", max_length=255)
    # 입출금 구분
    transaction_type = models.CharField(
        "Transaction Type", max_length=10, choices=TRANSACTION_TYPE
    )
    # ATM/계좌이체/카드결제 등 방법 구분
    transaction_method = models.CharField(
        "Transaction Method", max_length=20, choices=TRANSACTION_METHOD
    )

    transaction_timestamp = models.DateTimeField(
        "Transaction Timestamp", auto_now_add=True
    )  # 거래 일시

    class Meta:
        db_table = "transaction_history"
        indexes = [
            models.Index(fields=["account"]),
        ]

    def save(self, *args, **kwargs):
        if not self.pk:
            acct = self.account
            if self.transaction_type == "IN":
                acct.balance += self.transaction_amount
            else:
                acct.balance -= self.transaction_amount
            acct.save()
            self.post_transaction_amount = acct.balance
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.get_transaction_type_display()} "
            f"{self.transaction_amount}원 – "
            f"{self.transaction_timestamp:%Y-%m-%d %H:%M}"
        )
