from rest_framework import serializers
from user.models import Profile
from digest.models import ImageDigest, LinkDigest
from digest.serializers import ImageDigestSerializer, LinkDigestSerializer
from django.contrib.auth.models import User


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
