from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    # 쿠키에 저장된 access_token을 읽어 인증 처리하는 클래스
    def authenticate(self, request):
        # 헤더가 아닌 쿠키에서 토큰 추출
        raw_token = request.COOKIES.get("access_token")
        if raw_token is None:
            return None  # 토큰 없으면 인증 시도 안 함
        # 검증된 토큰 객체 생성
        validated_token = self.get_validated_token(raw_token)
        # 토큰에서 유저 가져와 반환
        return self.get_user(validated_token), validated_token
