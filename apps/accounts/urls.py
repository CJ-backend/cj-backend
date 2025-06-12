from django.urls import path

from .views import (
    AccountCreateView,
    AccountDeleteView,
    AccountRetrieveView,
    TransactionCreateView,
    TransactionDeleteView,
    TransactionRetrieveView,
    TransactionUpdateView,
)

app_name = "accounts"


urlpatterns = [
    path(
        "account/create/", AccountCreateView.as_view(), name="account-create"
    ),  # 계좌 생성
    path(
        "account/", AccountRetrieveView.as_view(), name="account-retrieve"
    ),  # 계좌 조회
    path(
        "account/<uuid:account_id>/delete/",
        AccountDeleteView.as_view(),
        name="account-delete",
    ),  # 계좌 삭제
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
