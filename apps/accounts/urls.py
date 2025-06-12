from django.urls import path
from .views import AccountCreateView, AccountRetrieveView, AccountUpdateView, TransactionCreateView

urlpatterns = [
    path('account/create/', AccountCreateView.as_view(), name='account-create'),  # 계좌 생성
    path('account/', AccountRetrieveView.as_view(), name='account-retrieve'),  # 계좌 조회
    path('account/update/', AccountUpdateView.as_view(), name='account-update'),  # 계좌 수정 불가
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction-create'),  # 거래 생성
]
