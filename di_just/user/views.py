from django.shortcuts import render

# Create your views here.
from user.serializers import RegisterSerializer, UserUpdateSerializer, PasswordUpdateSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import generics


class RegisterUser(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class PasswordUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PasswordUpdateSerializer


