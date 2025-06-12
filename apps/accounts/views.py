from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Account
from .serializers import AccountSerializer


class AccountCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        serializer = AccountSerializer(data=request.data)  # 전달된 데이터를 serializer로 변환
        if serializer.is_valid():  # 유효성 검사
            serializer.save(user=request.user)  # 계좌 생성 시 현재 사용자 정보와 함께 저장
            response_data = serializer.data
            response_data.pop('user', None)  # 'user' 필드 제외
            return Response(response_data, status=status.HTTP_201_CREATED)  # 성공적인 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 오류가 있는 경우


class AccountRetrieveView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=request.user)  # 모든 계좌 조회
        if accounts.exists():
            serializer = AccountSerializer(accounts, many=True)  # 여러 개의 계좌를 직렬화
            return Response(serializer.data)
        return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)


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
