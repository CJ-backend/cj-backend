from django.urls import path

from .views import (
    AccountCreateView,
    AccountDeleteView,
    AccountListView,
    TransactionCreateView,
    TransactionDeleteView,
    TransactionListView,
    TransactionUpdateView,
)

app_name = "accounts"


urlpatterns = [
    path(
        "accounts/create/", AccountCreateView.as_view(), name="account-create"
    ),  # 계좌 생성
    path("accounts/", AccountListView.as_view(), name="account-list"),  # 계좌 조회
    path(
        "accounts/<uuid:account_id>/delete/",
        AccountDeleteView.as_view(),
        name="account-delete",
    ),  # 계좌 삭제
    path(
        "transactions/create/",
        TransactionCreateView.as_view(),
        name="transaction-create",
    ),  # 거래 생성
    path(
        "transactions/", TransactionListView.as_view(), name="transaction-list"
    ),  # 거래 내역 조회
    path(
        "transactions/update/<uuid:transaction_id>/",
        TransactionUpdateView.as_view(),
        name="transaction-update",
    ),  # 거래 내역 수정
    path(
        "transactions/delete/<uuid:transaction_id>/",
        TransactionDeleteView.as_view(),
        name="transaction-delete",
    ),  # 거래 내역 삭제
]
