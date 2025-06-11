from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserProfileSerializer

User = get_user_model()


# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer  # RegisterSerializer 로 유저 생성 로직 위임


# 이메일 토큰
class ActivateView(generics.GenericAPIView):
    def get(self, request, uid, token):
        try:
            user = User.objects.get(user_id=uid)
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


# 쿠키 기반 refresh_token으로 access_token을 재발급
class CookieTokenRefreshView(APIView):
    #쿠키에 저장된 refresh_token 으로 access_token 재발급 후, HttpOnly 쿠키에 새로운 access_token 설정
    permission_classes = [IsAuthenticated]  # 인증된 사용자만

    def post(self, request, *args, **kwargs):
        # 1) 쿠키에서 refresh_token 꺼내기
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {"detail": "리프레시 토큰이 없습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2) RefreshToken 으로 검증 & 새 access 발급
        try:
            token = RefreshToken(refresh_token)
        except Exception:
            return Response(
                {"detail": "잘못된 토큰입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        new_access = str(token.access_token)  # 새 access 토큰 추출

        # 3) 응답 및 쿠키 세팅
        response = Response({"access": new_access}, status=status.HTTP_200_OK)
        response.set_cookie(
            key="access_token",
            value=new_access,
            httponly=True,
            samesite="Lax",
        )
        # refresh_token 은 블랙리스트 로직이 따로 있으면 그쪽에서 처리
        return response


# Refresh Token을 블랙리스트에 추가하고, 쿠키(access_token, refresh_token) 를 삭제하는 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 호출 가능

    def post(self, request, *args, **kwargs):
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


# 본인 프로필 조회·수정·삭제
class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # 본인 객체만

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        self.perform_destroy(user)
        return Response({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
