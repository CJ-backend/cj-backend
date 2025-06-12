from django.urls import path

from .views import (
    AccountCreateView,
    AccountRetrieveView,
    AccountUpdateView,
    TransactionCreateView,
    TransactionDeleteView,
    TransactionRetrieveView,
    TransactionUpdateView,
)

urlpatterns = [
    path(
        "account/create/", AccountCreateView.as_view(), name="account-create"
    ),  # 계좌 생성
    path(
        "account/", AccountRetrieveView.as_view(), name="account-retrieve"
    ),  # 계좌 조회
    path(
        "account/update/", AccountUpdateView.as_view(), name="account-update"
    ),  # 계좌 수정 불가
    path(
        "transaction/create/",
        TransactionCreateView.as_view(),
        name="transaction-create",
    ),  # 거래 생성
    path(
        "transactions/", TransactionRetrieveView.as_view(), name="transaction-retrieve"
    ),  # 거래 내역 조회
    path(
        "transaction/update/<int:pk>/",
        TransactionUpdateView.as_view(),
        name="transaction-update",
    ),  # 거래 내역 수정
    path(
        "transaction/delete/<int:pk>/",
        TransactionDeleteView.as_view(),
        name="transaction-delete",
    ),  # 거래 내역 삭제
]
