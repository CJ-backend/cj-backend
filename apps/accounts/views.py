from rest_framework import generics, permissions, serializers, status
from rest_framework.permissions import IsAuthenticated

from .models import Account, TransactionHistory
from .serializers import (
    AccountSerializer,
    TransactionPatchSerializer,
    TransactionSerializer,
)


# 미션 1: 계좌 생성 API
class AccountCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        return resp


# 미션 2: 계좌 조회 API
class AccountListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AccountSerializer

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


# 3) 계좌 삭제
class AccountDeleteView(generics.DestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "account_id"

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)


# 미션 4: 거래 생성 API
class TransactionCreateView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        # 1) 본인 계좌 조회
        account = Account.objects.filter(user=self.request.user).first()
        if not account:
            raise serializers.ValidationError("등록된 계좌가 없습니다.")

        # 2) 모델 save() 로만 입출금 로직 실행
        serializer.save(account=account)


# 미션 5: 거래 내역 조회 API
class TransactionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        qs = TransactionHistory.objects.filter(account__user=self.request.user)
        tp = self.request.query_params.get("transaction_type")
        if tp:
            qs = qs.filter(transaction_type=tp)
        mn = self.request.query_params.get("min_amount")
        if mn:
            qs = qs.filter(transaction_amount__gte=mn)
        mx = self.request.query_params.get("max_amount")
        if mx:
            qs = qs.filter(transaction_amount__lte=mx)
        return qs


# 거래 내역 수정 API
class TransactionUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionPatchSerializer
    lookup_field = "pk"
    http_method_names = ["patch"]

    def get_queryset(self):
        return TransactionHistory.objects.filter(account__user=self.request.user)


# 거래 내역 삭제 API
class TransactionDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return TransactionHistory.objects.filter(account__user=self.request.user)
