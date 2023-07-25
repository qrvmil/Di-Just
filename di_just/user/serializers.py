from rest_framework import serializers
from user.models import Profile
from digest.models import ImageDigest, LinkDigest
from digest.serializers import ImageDigestSerializer, LinkDigestSerializer
from django.contrib.auth.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2']

    def save(self, *args, **kwargs):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Different passwords"})
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    # created_img_digest = ImageDigestSerializer(many=True, read_only=True)
    # created_link_digest = LinkDigestSerializer(many=True, read_only=True)
    # saved_img_digest = ImageDigestSerializer(many=True, read_only=True)
    # saved_link_digest = LinkDigestSerializer(many=True, read_only=True)
    # user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'picture', 'bio', 'age', 'follows', 'created_timestamp']

    def validate(self, attrs):
        print(attrs)
        return attrs
