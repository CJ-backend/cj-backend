from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="password123",
            name="테스터",
            nickname="tester",
        )
        self.login_url = reverse("users:login")
        self.profile_url = reverse("users:me")

        # access_token (force_authenticate로 처리됨)
        self.client.force_authenticate(user=self.user)

        # refresh_token 수동 쿠키 설정 (로그아웃을 위해)
        refresh = RefreshToken.for_user(self.user)
        self.client.cookies["refresh_token"] = str(refresh)

    def test_register_user(self):
        # 회원가입은 인증 없이 요청해야 하므로 force_authenticate 해제
        self.client.force_authenticate(user=None)

        url = reverse("users:register")
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "nickname": "newbie",
            "name": "새유저",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_login_and_profile_access(self):
        # force_authenticate로 이미 로그인 상태이므로 바로 접근 가능
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], "tester")

    def test_profile_patch(self):
        data = {"name": "이름수정"}
        response = self.client.patch(self.profile_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "이름수정")

    def test_logout(self):
        logout_url = reverse("users:logout")
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
