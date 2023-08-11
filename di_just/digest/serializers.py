from rest_framework import serializers
from digest.models import ImageDigest, LinkDigest, Topics, DigestLinks, DigestImages, Comments
from user.models import Profile


# TO DO: дайджесты + правильное сохранение картинок


class DigestImageUpdateSerializer(serializers.ModelSerializer):
    # вызывается непосредственно при обновлении дайджеста, поэтому в сериализаторе дайджест не прописывается
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


class DigestImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigestImages
        fields = ["id", "digest", "picture"]


class ImageDigestCreateSerializer(serializers.ModelSerializer):
    pictures = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True), write_only=True
    )
    descriptions = serializers.ListField(
        child=serializers.CharField(), write_only=True
    )
    public = serializers.BooleanField(default=True)

    # topic = serializers.PrimaryKeyRelatedField(many=True, required=False)
    # TO DO: разобраться с topic
    class Meta:
        model = ImageDigest
        fields = ['id', 'owner', 'introduction', 'name', 'conclusion', 'public', 'pictures', 'descriptions']

        extra_kwargs = {
            'pictures': {'required': True},
            'owner': {'required': False},
            'name': {'required': False},
            'introduction': {'required': False},
            'conclusion': {'required': False},
            'descriptions': {'required': False},
            'public': {'required': False}
        }

    def create(self, validated_data):
        pictures = validated_data.pop("pictures")
        descriptions = validated_data.pop("descriptions")

        digest = ImageDigest.objects.create(**validated_data)
        for picture, description in zip(pictures, descriptions):
            DigestImages.objects.create(digest=digest, picture=picture, description=description)

        return digest


class ImageDigestUpdateSerializer(serializers.ModelSerializer):
    pictures = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True), write_only=True, required=False
    )
    descriptions = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    public = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = ImageDigest
        fields = ['id', 'owner', 'introduction', 'name', 'conclusion', 'public', 'pictures', 'descriptions']

        extra_kwargs = {
            'owner': {'required': False},
            'name': {'required': False},
            'introduction': {'required': False},
            'conclusion': {'required': False},
            'descriptions': {'required': False},
            'public': {'required': False}
        }

    # NB из формы в запрос возвращаем все данные из pictures и descriptions, а не только измененные
    def update(self, instance, validated_data):




        instance.introduction = validated_data.get("introduction", instance.introduction)
        instance.name = validated_data.get("name", instance.name)
        instance.conclusion = validated_data.get("conclusion", instance.conclusion)
        instance.public = validated_data.get("public", instance.public)
        instance.save()
        return instance


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

    class Meta:ы 
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
