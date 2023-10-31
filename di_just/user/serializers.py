from django.contrib.auth import authenticate
from rest_framework import serializers
from user.models import Profile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


# TO DO: разобраться с тем, где правильнее прописывать get и create (serializer/view)
# register user
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #         first_name=validated_data['first_name'],
    #         last_name=validated_data['last_name']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user


# login user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if not user:
            raise serializers.ValidationError("username or password Incorrect")

        return data


# update user info
class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())], required=False
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'username': {'required': False},
        }

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()
        return instance


# update user password
class PasswordUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True)

    class Meta:
        model = User
        fields = ['password']

    def update(self, instance, validated_data):
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


# shows authenticated user his/her user info (delete user)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


# update profile
class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['bio', 'age', 'follows']


class ProfilePictureUpdateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Profile
        fields = ['picture', 'user']

    def update(self, instance, validated_data):
        if instance.picture != "":
            storage, path = instance.picture.storage, instance.picture.path
            storage.delete(path)
        instance.picture = validated_data["picture"]
        instance.save()
        return instance


# retrieve and delete profile
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'picture', 'bio', 'age', 'follows', 'followed_by']


# list all profiles
class ProfileListSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Profile
        fields = ['id', 'user', 'picture', 'bio', 'follows', 'followed_by']
