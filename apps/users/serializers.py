from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # 이메일 중복 시 에러 메시지 출력
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="이미 사용 중인 이메일입니다."
            )
        ]
    )
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
        uid = user.user_id
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


# 프로필 조회·수정·삭제
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "nickname", "name", "phone_number")
        read_only_fields = ("email",)  # 이메일은 변경 불가
