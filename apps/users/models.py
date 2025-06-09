from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    # 일반 유저 메서드
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("이메일을 입력해주세요")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 슈퍼 유저 생성 메서드
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    # 커스텀 유저 모델
    email = models.EmailField('이메일',max_length=255, unique=True)
    nickname = models.CharField('닉네임',max_length=20, unique=True)
    name = models.CharField('이름',max_length=30)
    phone_number = models.CharField('전화번호',max_length=11, blank=True, null=True)
    # AbstractBaseUser를 상속할때 password, last_login을 제공
    # last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField('계정 활성화',default=True)
    is_staff = models.BooleanField('스태프 여부',default=False)
    is_superuser = models.BooleanField('관리자 여부',default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "name"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email