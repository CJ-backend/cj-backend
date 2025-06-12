from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    # 쿠키에 저장된 access_token을 읽어 인증 처리하는 클래스
    def authenticate(self, request):
        # 헤더가 아닌 쿠키에서 토큰 추출
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None  # 토큰 없으면 인증 시도 안 함
        try:
            validated_token = self.get_validated_token(raw_token)
        except Exception:
            # 토큰 만료·오류 등 문제 발생 시 무시하고 anonymous 처리
            return None
        return self.get_user(validated_token), validated_token
