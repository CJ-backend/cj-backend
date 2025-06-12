from django.urls import path

from .views import (
    ActivateView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
    ProfileView,
    RegisterView,
)

app_name = "users"

urlpatterns = [
    # 회원가입
    path("register/", RegisterView.as_view(), name="register"),
    # 이메일 인증
    path(
        "activate/<uuid:uid>/<str:token>/", ActivateView.as_view(), name="user-activate"
    ),
    # 내 프로필 조회·수정·삭제
    path("me/", ProfileView.as_view(), name="me"),
    # 인증(auth)
    # 로그인 → 쿠키에 JWT 저장
    path("auth/login/", CookieTokenObtainPairView.as_view(), name="login"),
    # 리프레시 → 새 access 토큰 발급
    path("auth/refresh/", CookieTokenRefreshView.as_view(), name="refresh"),
    # 로그아웃 → 리프레시 블랙리스트 + 쿠키 삭제
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
