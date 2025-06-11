"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from apps.users.views import (
    ActivateView,
    CookieTokenObtainPairView,
    CookieTokenRefreshView,
    LogoutView,
    RegisterView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # apps 단위로 URL 분리 시 예시
    # path("api/", include("apps.myapp.urls")),
]

# 개발 모드에서만 Swagger 문서 라우팅 추가
if settings.DEBUG:

    schema_view = get_schema_view(
        openapi.Info(
            title="Django Mini Project API",
            default_version="v1",
            description="API for Django Mini Project",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@local.dev"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    urlpatterns += [
        # JSON / YAML schema
        path(
            "swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"
        ),
        path(
            "swagger.yaml", schema_view.without_ui(cache_timeout=0), name="schema-yaml"
        ),
        # Swagger UI
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="swagger-ui",
        ),
        # Redoc UI
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
        # 기존 라우팅
        path("api/v1/users/", include("apps.users.urls", namespace="users")),
        # 회원가입, 활성화
        path("api/v1/users/register/", RegisterView.as_view(), name="user-register"),
        path(
            "api/v1/users/activate/<uuid:uid>/<str:token>/",
            ActivateView.as_view(),
            name="user-activate",
        ),
        # JWT 로그인/토큰 갱신
        path(
            "api/v1/auth/login/",
            CookieTokenObtainPairView.as_view(),
            name="token_obtain_pair",
        ),
        path(
            "api/v1/auth/refresh/",
            CookieTokenRefreshView.as_view(),
            name="token_refresh",
        ),
        # 로그아웃 (Refresh Token 블랙리스트 + 쿠키 삭제)
        path("api/v1/auth/logout/", LogoutView.as_view(), name="token_logout"),
    ]
