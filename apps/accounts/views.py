from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Account, TransactionHistory
from .serializers import AccountSerializer, TransactionHistorySerializer

# 계좌 생성 API
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


# 계좌 조회 API
class AccountRetrieveView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, *args, **kwargs):
        accounts = Account.objects.filter(user=request.user)  # 모든 계좌 조회
        if accounts.exists():
            serializer = AccountSerializer(accounts, many=True)  # 여러 개의 계좌를 직렬화
            return Response(serializer.data)
        return Response({"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND)


# 계좌 수정 불가 API
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


# 거래 생성 API
class TransactionCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        # 요청에서 거래 정보 받아오기
        serializer = TransactionHistorySerializer(data=request.data)

        if serializer.is_valid():  # 유효성 검사
            transaction_type = serializer.validated_data['transaction_type']  # 거래 유형
            transaction_amount = serializer.validated_data['transaction_amount']  # 거래 금액
            account = Account.objects.get(user=request.user)  # 현재 로그인된 사용자의 계좌

            # 거래 유형에 맞게 계좌 잔액 업데이트
            if transaction_type == 'IN':
                account.balance += transaction_amount  # 입금
            elif transaction_type == 'OUT':
                if account.balance >= transaction_amount:
                    account.balance -= transaction_amount  # 출금
                else:
                    return Response({"detail": "Insufficient balance."}, status=status.HTTP_400_BAD_REQUEST)

            account.save()  # 계좌 잔액 저장

            # 거래 내역 저장
            serializer.save(account=account)  # 거래 내역 저장 시 계좌 정보 연결

            return Response(serializer.data, status=status.HTTP_201_CREATED)  # 성공적인 응답
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 유효하지 않은 데이터가 들어온 경우
