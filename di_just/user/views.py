from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from user.serializers import RegisterSerializer, UserUpdateSerializer, PasswordUpdateSerializer, \
    ProfileUpdateSerializer, ProfileSerializer, UserSerializer, ProfileListSerializer, LoginSerializer, \
    ProfilePictureUpdateSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.views import APIView
from user.models import Profile
from user.custom_permissions import IsOwner, IsSameUser
from knox.models import AuthToken
from django.core.mail import EmailMessage, send_mail
from django.utils.encoding import force_str
from user.token import account_activation_token
from user.pagination import CustomPagination


class RegisterUserAPI(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    # регистрвция нового пользователя
    # request -- данные с клиента
    def post(self, request, *args, **kwargs):
        user_serializer = self.get_serializer(data=request.data)
        # сериализация и валидация данных
        user_serializer.is_valid(raise_exception=True)
        # user = user_serializer.save()
        # создание пользователя
        user = User.objects.create(
            username=user_serializer.validated_data['username'],
            email=user_serializer.validated_data['email'],
            first_name=user_serializer.validated_data['first_name'],
            last_name=user_serializer.validated_data['last_name']
        )
        user.set_password(user_serializer.validated_data['password'])
        user.save()

        # отправка письма со ссылкой для верификации аккаунта
        current_site = 'http://localhost:3000'  # get_current_site(request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': current_site[7:],  # current_site.domain,
            'uid': user.pk,
            'token': account_activation_token.make_token(user),
        })
        to_email = user.email
        send_mail(mail_subject, message, 'di-just-info@yandex.ru', [to_email], fail_silently=False)
        return Response({"email has been sent"})


class ActivateAPI(APIView):
    # данная функция ловит ссылку валидаци, и в случае успеха активирует аккаунт
    def put(self, request, uid, token):
        try:
            # uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.profile.is_verified = True
            user.profile.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    # функция для входа пользователя в систему
    # request -- данные с сервера

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.get(username=username)

        if user.profile.is_verified:

            return Response({
                'user': user.id,  # UserSerializer(user).data,
                'token': AuthToken.objects.create(user)[1]
            })

        else:
            return Response({"error": "your profile is not verified"})


class UserUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsSameUser]
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer


class PasswordUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsSameUser]
    queryset = User.objects.all()
    serializer_class = PasswordUpdateSerializer


class ProfileRestoreEmailAPI(APIView):
    permission_classes = [AllowAny]  # [IsSameUser]
    queryset = User.objects.all()
    serializer_class = PasswordUpdateSerializer

    # данная функция отвечает за отправку письма со ссылкой для восстановления пароля

    def put(self, request):
        email = request.data["email"]
        user = User.objects.get(email=email)
        current_site = 'http://localhost:3000'  # get_current_site(request)
        mail_subject = 'Please follow the link to reset the password for your account'
        message = render_to_string('pass_reset_email.html', {
            'user': user,
            'domain': current_site[7:],  # current_site.domain,
            'uid': user.pk,  # urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = email  # user.email
        send_mail(mail_subject, message, 'di-just-info@yandex.ru', [to_email], fail_silently=False)

        return Response({"email has been sent"})


class ProfileRestoreAPI(APIView):

    # данная функция восстанавливает аккаунт пользователя и присваивает ему новый пароль

    def put(self, request, uid, token):
        try:
            # uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            password = request.data["password"]
            user.set_password(password)
            user.save()
            return HttpResponse('OK')
        else:
            return HttpResponse('Activation link is invalid!')


class ProfileUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer


class ProfilePictureUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfilePictureUpdateSerializer


class ProfileInfoAPI(generics.RetrieveDestroyAPIView):
    permission_classes = [IsOwner]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileGetInfo(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserInfoAPI(generics.RetrieveDestroyAPIView):
    permission_classes = [IsSameUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileListAPI(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    pagination_class = CustomPagination


class FollowUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    # функция обрабатывает подписку на определенного пользователя
    def put(self, request, pk):
        follow = Profile.objects.get(pk=pk)
        request.user.profile.follows.add(follow)

        return Response({f"Now you follow {follow.user.username}"})


class UnfollowUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    # функция обрабатывает отписку от определенного пользователя

    def put(self, request, pk):
        unfollow = Profile.objects.get(pk=pk)
        request.user.profile.follows.remove(unfollow)

        return Response({f"You unfollowed {unfollow.user.username}"})
