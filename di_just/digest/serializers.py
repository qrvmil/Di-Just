from rest_framework import serializers
from digest.models import ImageDigest, LinkDigest, Topics, DigestLinks, DigestImages, Comments
from user.models import Profile


# TODO: получение всех сохраненных юзером дайджестов
# TODO: получение дайджестов по топикам
# TODO: добавить топики
# TODO: добавить комментарии


class DigestImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigestImages
        fields = ['picture', 'description']

        extra_kwargs = {
            'picture': {'required': True},
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


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ["topic_name"]


class ImageDigestCreateSerializer(serializers.ModelSerializer):
    pictures = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True), write_only=True, required=False
    )
    descriptions = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    public = serializers.BooleanField(default=True)

    # topic = serializers.PrimaryKeyRelatedField(many=True, required=False)
    # TODO: разобраться с topic
    class Meta:
        model = ImageDigest
        fields = ['id', 'owner', 'introduction', 'name', 'conclusion', 'public', 'pictures', 'descriptions']

        extra_kwargs = {
            'owner': {'required': False},
            'name': {'required': False},
            'introduction': {'required': False},
            'conclusion': {'required': False},
            'public': {'required': False}
        }

    # в api всегда должны передаваться оба параметра pictures и descriptions, причем одинакового размера
    def create(self, validated_data):

        if "pictures" in validated_data.keys() and "descriptions" in validated_data.keys():
            pictures = validated_data.pop("pictures")
            descriptions = validated_data.pop("descriptions")

            digest = ImageDigest.objects.create(**validated_data)
            for picture, description in zip(pictures, descriptions):
                DigestImages.objects.create(digest=digest, picture=picture, description=description)
        else:
            digest = ImageDigest.objects.create(**validated_data)

        return digest


class ImageDigestRetrieveDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageDigest
        fields = ['owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user', 'text', 'created_timestamp', 'link_digest', 'img_digest']


class DigestLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigestImages
        fields = ['id', 'digest', 'link', 'description']


class LinkDigestCreateSerializer(serializers.ModelSerializer):
    links = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    descriptions = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    public = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = LinkDigest
        fields = ['owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp',
                  'links', 'descriptions']

    def create(self, validated_data):

        if "links" in validated_data.keys() and "descriptions" in validated_data.keys():
            links = validated_data.pop("links")
            descriptions = validated_data.pop("descriptions")

            digest = LinkDigest.objects.create(**validated_data)
            for link, description in zip(links, descriptions):
                DigestLinks.objects.create(digest=digest, link=link, description=description)
        else:
            digest = LinkDigest.objects.create(**validated_data)

        return digest


class ListDigestSerializer