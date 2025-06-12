from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Account
from .serializers import AccountSerializer

class AccountCreateView(generics.CreateAPIView):
    queryset = Account.objects.all()  # 모든 Account 객체를 다룰 수 있게 설정
    serializer_class = AccountSerializer  # 사용할 시리얼라이저 지정
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능하도록 설정

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


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