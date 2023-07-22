from rest_framework import serializers
from user.models import Profile
from digest.models import ImageDigest, LinkDigest
from digest.serializers import ImageDigestSerializer, LinkDigestSerializer
from django.contrib.auth.models import User

'''
не забудь пофиксить, что topic не отображается !!!
'''


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    created_img_digest = ImageDigestSerializer(many=True, read_only=True)
    created_link_digest = LinkDigestSerializer(many=True, read_only=True)
    saved_img_digest = ImageDigestSerializer(many=True, read_only=True)
    saved_link_digest = LinkDigestSerializer(many=True, read_only=True)
    user = UserSerializer(many=False)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'picture', 'bio', 'age', 'follows', 'created_timestamp', 'created_img_digest',
                  'created_link_digest', 'saved_img_digest', 'saved_link_digest']

    '''
    не работает


    def create(self, validated_data):
        created_img_digest_data = validated_data.pop('created_img_digest')
        created_link_digest_data = validated_data.pop('created_link_digest')
        saved_img_digest_data = validated_data.pop('saved_img_digest')
        saved_link_digest_data = validated_data.pop('saved_link_digest')

        new_profile = Profile.objects.create(**validated_data)

        for single_digest_data in created_img_digest_data:
            ImageDigest.objects.create(owner=new_profile, **single_digest_data)

        for single_digest_data in created_link_digest_data:
            ImageDigest.objects.create(owner=new_profile, **single_digest_data)

        # for single_digest_data in saved_img_digest_data:
        #     ImageDigest.objects.create(owner=new_profile, **single_digest_data)
        #
        # for single_digest_data in saved_link_digest_data:
        #     ImageDigest.objects.create(owner=new_profile, **single_digest_data)

        return new_profile

    def update(self, instance, validated_data):
        pass
    '''
