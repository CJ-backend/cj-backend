import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    # 일반 유저 메서드
    def create_user(self, email, password=None, name=None, **extra_fields):
        if not email:
            raise ValueError("이메일을 입력해주세요")
        email = self.normalize_email(email)
        user = self.model(
            id=uuid.uuid4(), email=email, name=name, is_active=False, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 슈퍼 유저 생성 메서드
    def create_superuser(self, email, password, name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("슈퍼유저는 is_staff=True 이어야 합니다.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("슈퍼유저는 is_superuser=True 이어야 합니다.")

        return self.create_user(email, password, name, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    # 커스텀 유저 모델
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField("이메일", max_length=255, unique=True)
    nickname = models.CharField("닉네임", max_length=20, unique=True)
    name = models.CharField("이름", max_length=30)
    phone_number = models.CharField("전화번호", max_length=11, blank=True, null=True)
    # AbstractBaseUser를 상속할때 password, last_login을 제공
    # last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField("계정 활성화", default=False)
    is_staff = models.BooleanField("스태프 여부", default=False)
    is_superuser = models.BooleanField("관리자 여부", default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email
