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
from rest_framework import authentication, permissions

urlpatterns = [
    path("admin/", admin.site.urls),
    # user 매핑
    path("api/v1/users/", include("apps.users.urls", namespace="users")),
    # account 매핑
    path("api/v1/accounts/", include("apps.accounts.urls", namespace="accounts")),
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
        public=False,
        authentication_classes=[
            authentication.SessionAuthentication,  # 세션 인증
        ],
        permission_classes=[permissions.IsAuthenticated],  # 인증된 사용자만 접근 가능
    )

    # Swagger UI 관련 경로 추가
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
    ]
