import os

from dotenv import load_dotenv

from .base import *

load_dotenv()

DEBUG = os.getenv("DJANGO_DEBUG", "False") == "True"

# 실제 서비스 도메인(환경변수 또는 직접 작성)
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(",")

# 실제 프로덕션 DB 환경변수(ex: PostgreSQL)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST", "127.0.0.1"),
        "PORT": os.getenv("POSTGRES_PORT", "5432"),
    }
}

# Static / Media 파일을 위한 외부 스토리지 설정 등
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "mediafiles"

# 프로덕션 미디어 URL
MEDIA_URL = "/media/"

# 보안 관련 설정 예시
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
