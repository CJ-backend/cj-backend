from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer

User = get_user_model()


# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer  # RegisterSerializer 로 유저 생성 로직 위임


# 이메일 토큰
class ActivateView(generics.GenericAPIView):
    def get(self, request, uid, token):
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response(
                {"detail": "유효하지 않은 사용자입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(user, token):  # 토큰 검증
            user.is_active = True  # 활성화 플래그 변경
            user.save()
            return Response(
                {"detail": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "토큰이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )


# 로그인 시 JWT를 발급하고, 쿠키에 저장
class CookieTokenObtainPairView(TokenObtainPairView):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            # access_token을 HttpOnly 쿠키로 저장
            response.set_cookie(
                key="access_token",
                value=data.get["access"],
                httponly=True,
                samesite="Lax",
            )
            # refresh_token을 HttpOnly 쿠키로 저장
            response.set_cookie(
                key="refresh_token",
                value=data.get["refresh"],
                httponly=True,
                samesite="Lax",
            )
            #  body에서 토큰 제거: response.data = {}
        return response


# 쿠키 기반 refresh_token으로 access_token을 재발급
class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            # 새로운 access_token을 쿠키에 업데이트
            response.set_cookie(
                key="access_token",
                value=data.get["access"],
                httponly=True,
                samesite="Lax",
            )
            # refresh_token은 그대로 유지
        return response


# Refresh Token을 블랙리스트에 추가하고, 쿠키(access_token, refresh_token) 를 삭제하는 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 호출 가능

    def post(self, request):
        # 1) 쿠키에서 refresh_token 꺼내기
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "리프레시 토큰이 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2) 토큰 블랙리스트에 추가
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"detail": "잘못된 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 3) 쿠키 삭제 후 응답
        response = Response(
            {"detail": "로그아웃 되었습니다."}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
