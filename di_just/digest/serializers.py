from rest_framework import serializers
from digest.models import ImageDigest, LinkDigest, Topics, DigestLinks, DigestImages, Comments


# TO DO: дайджесты + правильное сохранение картинок


class DigestImageUpdateSerializer(serializers.ModelSerializer):
    # вызывается непосредственно при обновлении дайджеста, поэтому в сериализаторе дайджест не прописывается
    class Meta:
        model = DigestImages
        fields = ['picture', 'description']

        extra_kwargs = {
            'picture': {'required': False},
            'description': {'required': False},
        }

    def update(self, instance, validated_data):
        if 'picture' in validated_data and instance.picture != validated_data["picture"]:
            storage, path = instance.picture.storage, instance.picture.path
            storage.delete(path)
            instance.picture = validated_data.get("picture", instance.picture)

        instance.description = validated_data.get("description", instance.description)
        instance.save()
        return instance


class DigestImageCRDSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigestImages
        fields = ['id', 'digest', 'picture', 'description']





'''
class DigestLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigestLinks
        fields = ['digest', 'link', 'description']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user', 'text', 'created_timestamp']


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['topic_name']


class ImageDigestSerializer(serializers.ModelSerializer):
    images = DigestImageSerializer(many=True)
    comments = CommentsSerializer(many=True)
    topic = serializers.StringRelatedField(many=True)

    class Meta:
        model = ImageDigest
        fields = ['owner', 'introduction', 'name', 'conclusion', 'saves', 'public', 'created_timestamp',
                  'images', 'topic', 'comments']

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class LinkDigestSerializer(serializers.ModelSerializer):
    links = DigestLinkSerializer(many=True)
    comments = CommentsSerializer(many=True)
    topics = serializers.StringRelatedField(many=True)

    class Meta:
        model = LinkDigest
        fields = ['owner', 'introduction', 'name', 'conclusion', 'saves', 'public', 'created_timestamp',
                  'links', 'topics', 'comments']

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
'''
