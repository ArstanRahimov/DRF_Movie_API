from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (RegistrationSerializer, ActivationSerializer,
                          LoginSerializer, ChangePasswordSerializer,
                          ForgotPasswordSerializer, ForgotPasswordCompleteSerializer)


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegistrationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.create()
        return Response('Вы успешно зарегистрировались', status=201)


class ActivationView(APIView):
    def post(self, requset):
        data = requset.data
        serializer = ActivationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('Ваш аккаунт успешно активирован')


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        # Token.objects.filter(user=user).delete()
        user.auth_token.delete()  # auth_token - related_name у класса Token
        return Response('Вы успешно разлогинились')


class ChangePasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ChangePasswordSerializer(data=data,
                                              context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно обновлен')


class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Вам выслан код подтверждения')


class ForgotPasswordCompleteView(APIView):
    def post(self, request):
        data = request.data
        serializer = ForgotPasswordCompleteSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль успешно восстановлен')



