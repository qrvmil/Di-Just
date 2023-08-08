from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.serializers import RegisterSerializer, UserUpdateSerializer, PasswordUpdateSerializer, \
    ProfileUpdateSerializer, ProfileSerializer, UserSerializer, ProfileListSerializer, LoginSerializer, \
    ProfilePictureUpdateSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import generics
from user.models import Profile
from user.custom_permissions import IsOwner, IsSameUser
from knox.models import AuthToken


# TO DO: продумать логику сортировщика
class RegisterUser(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        # user = user_serializer.save()

        user = User.objects.create(
            username=user_serializer.validated_data['username'],
            email=user_serializer.validated_data['email'],
            first_name=user_serializer.validated_data['first_name'],
            last_name=user_serializer.validated_data['last_name']
        )
        user.set_password(user_serializer.validated_data['password'])
        user.save()

        return Response({
            'user': RegisterSerializer(user).data,
            'token': AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.get(username=username)

        return Response({
            'user': UserSerializer(user).data,
            'token': AuthToken.objects.create(user)[1]
        })


class UserUpdate(generics.UpdateAPIView):
    permission_classes = [IsSameUser]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class PasswordUpdate(generics.UpdateAPIView):
    permission_classes = [IsSameUser]
    queryset = User.objects.all()
    serializer_class = PasswordUpdateSerializer


class ProfileUpdate(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer


class ProfilePictureUpdate(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfilePictureUpdateSerializer


class ProfileInfo(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserInfo(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileList(generics.ListAPIView):
    # TO DO: NB!! когда будешь прописывать сортировщика продумать как правильно отдавать queryset
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
