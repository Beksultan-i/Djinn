from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .models import MyUser
from .serializers import RegisterSerializers, LoginSerializer, CreateNewPasswordSerializer
from .utils import send_activation_code


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializers(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully signed up!', status=status.HTTP_201_CREATED)
        return Response('Not valid', status=status.HTTP_400_BAD_REQUEST)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(MyUser, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response("Your account successfully activated!", status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)


class ForgotPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        print(email)
        user = get_object_or_404(MyUser, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code(email=email, activation_code=user.activation_code)
        return Response('На Вашу почту отправлен код активации', status=status.HTTP_200_OK)


class ForgotPasswordComplete(APIView):
    def post(self, request):
        data = request.data
        serializer = CreateNewPasswordSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Вы успешно восстановили пароль', status=status.HTTP_200_OK)