from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 개발용 추가 INSTALLED_APPS
INSTALLED_APPS += [
    "drf_yasg",  # Swagger 문서 자동화 라이브러리
]

# 개발용 미들웨어 추가
MIDDLEWARE += []

STATIC_URL = "/static/"

# 개발용 정적 파일 디렉터리 설정
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 개발용 미디어 설정
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# 이메일 백엔드 등 개발 전용 설정(콘솔 출력 등)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
