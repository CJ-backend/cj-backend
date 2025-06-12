from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .serializers import AccountSerializer

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import status


class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()  # 모든 Account 객체를 다룰 수 있게 설정
    serializer_class = AccountSerializer  # 사용할 시리얼라이저 지정
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능하도록 설정

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountRetrieveView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, *args, **kwargs):
        try:
            # 현재 로그인된 사용자의 첫 번째 계좌 정보
            account = Account.objects.get(user=request.user)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except Account.DoesNotExist:
            return Response({"detail": "Account not found."}, status=404)


class AccountUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def put(self, request, *args, **kwargs):
        try:
            account = Account.objects.get(user=request.user)
            # 계좌가 이미 존재하면 수정 불가능하므로 오류 반환
            return Response(
                {"detail": "Account information cannot be updated."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."},
                status=status.HTTP_404_NOT_FOUND,
            )