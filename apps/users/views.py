from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import RegisterSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivateView(generics.GenericAPIView):
    def get(self, request, uid, token):
        try:
            user = User.objects.get(id=uid)
        except User.DoesNotExist:
            return Response(
                {"detail": "유효하지 않은 사용자입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {"detail": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK
            )

        return Response(
            {"detail": "토큰이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
