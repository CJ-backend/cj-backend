from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.response import Response
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


class CookieTokenObtainPairView(TokenObtainPairView):
    # 로그인 시 JWT를 발급하고, 쿠키에 저장
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            # access_token을 HttpOnly 쿠키로 저장
            response.set_cookie(
                key="access_token",
                value=data.get("access"),
                httponly=True,
                samesite="Lax",
            )
            # refresh_token을 HttpOnly 쿠키로 저장
            response.set_cookie(
                key="refresh_token",
                value=data.get("refresh"),
                httponly=True,
                samesite="Lax",
            )
            #  body에서 토큰 제거: response.data = {}
        return response


class CookieTokenRefreshView(TokenRefreshView):
    # 쿠키 기반 refresh_token으로 access_token을 재발급
    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            data = response.data
            # 새로운 access_token을 쿠키에 업데이트
            response.set_cookie(
                key="access_token",
                value=data.get("access"),
                httponly=True,
                samesite="Lax",
            )
            # refresh_token은 그대로 유지
        return response
