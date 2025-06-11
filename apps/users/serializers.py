from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = User
        fields = ("email", "name", "password")  # 필요한 필드 지정

    def create(self, validated_data):
        # is_active=False 상태로 유저 생성
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            name=validated_data["name"],
        )
        # 이메일 인증 토큰 생성
        token = default_token_generator.make_token(user)
        uid = user.id
        req = self.context.get("request")
        link = f"{req.scheme}://{req.get_host()}/api/v1/users/activate/{uid}/{token}/"

        # 이메일 발송 (콘솔 또는 SMTP)
        send_mail(
            subject="회원가입 인증 메일입니다",
            message=f"아래 링크를 클릭해 이메일 인증을 완료하세요:\n{link}",
            from_email=None,
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user
