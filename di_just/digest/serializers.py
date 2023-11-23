from rest_framework import serializers
from digest.models import ImageDigest, LinkDigest, Topics, DigestLinks, DigestImages, Comments
from user.models import Profile


# в данном файле представлены сериализаторы для моделей дайджеста


# сериализатор топиков (тегов)
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ["topic_name"]


# сериализатор создания комментариев
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user', 'text', 'created_timestamp', 'link_digest', 'img_digest']


# сериализатор для списка комментариев
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ['user', 'text', 'created_timestamp']


class DigestImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigestImages
        fields = ['picture', 'description']

        extra_kwargs = {
            'picture': {'required': True},
            'description': {'required': False},
        }

    # данная функция отвечает за обновление дайджеста картинками
    # в качестве аргументов принимает объект дайджеста, который нужно обновить и
    # validated_data -- информмвцию, на которую следуюет заменить текущую
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


# сериализатор для создания дайджеста картинками
class ImageDigestCreateSerializer(serializers.ModelSerializer):
    pictures = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True), write_only=True, required=False
    )
    descriptions = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )
    public = serializers.BooleanField(default=True)

    class Meta:
        model = ImageDigest
        fields = ['id', 'owner', 'introduction', 'name', 'conclusion', 'public', 'pictures', 'descriptions', 'topic']

        extra_kwargs = {
            'owner': {'required': False},
            'name': {'required': False},
            'introduction': {'required': False},
            'conclusion': {'required': False},
            'public': {'required': False}
        }

    # в api всегда должны передаваться оба параметра pictures и descriptions, причем одинакового размера
    # данная функция отвечает за создание дайджеста картинками
    # validated_data -- данные из сериализатора
    def create(self, validated_data):
        topics = []
        if "topic" in validated_data.keys():
            # достаем из данных, прошедших сериализацию, теги
            topics = validated_data.pop("topic")

        # достаем из данных, прошедших сериализацию, ссылки и описания к ним
        if "pictures" in validated_data.keys() and "descriptions" in validated_data.keys():
            pictures = validated_data.pop("pictures")
            descriptions = validated_data.pop("descriptions")

            # создание дайджеста
            digest = ImageDigest.objects.create(**validated_data)
            user = self.context['request'].user.profile
            digest.owner = user

            for picture, description in zip(pictures, descriptions):
                DigestImages.objects.create(digest=digest, picture=picture, description=description)
        else:
            digest = ImageDigest.objects.create(**validated_data)
            user = self.context['request'].user.profile
            digest.owner = user

        for topic in topics:
            digest.topic.add(topic)
        digest.save()
        return digest


class ImageDigestRetrieveDeleteSerializer(serializers.ModelSerializer):
    topic = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='topic_name'
    )

    class Meta:
        model = ImageDigest
        fields = ['owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp']


class ImageDigestListSerializer(serializers.ModelSerializer):
    topic = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='topic_name'
    )
    images = DigestImageCRDSerializer(many=True)

    class Meta:
        model = ImageDigest
        fields = ['id', 'owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp',
                  'images']


class DigestLinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigestLinks
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
        fields = ['owner', 'introduction', 'name', 'topic', 'conclusion', 'public', 'created_timestamp',
                  'links', 'descriptions']

    # данная функция отвечает за создание дайджеста ссылками
    # validated_data -- данные из сериализатора
    def create(self, validated_data):

        topics = []
        if "topic" in validated_data.keys():
            # достаем из данных, прошедших сериализацию, теги
            topics = validated_data.pop("topic")

        # достаем из данных, прошедших сериализацию, ссылки и описания к ним
        if "links" in validated_data.keys() and "descriptions" in validated_data.keys():
            links = validated_data.pop("links")
            descriptions = validated_data.pop("descriptions")

            # создаем новый дайджест
            digest = LinkDigest.objects.create(**validated_data)
            user = self.context['request'].user.profile
            digest.owner = user
            for link, description in zip(links, descriptions):
                DigestLinks.objects.create(digest=digest, link=link, description=description)
        else:
            digest = LinkDigest.objects.create(**validated_data)
            user = self.context['request'].user.profile
            digest.owner = user

        for topic in topics:
            # каждый тег добавляем отдельно в дайджест
            digest.topic.add(topic)

        digest.save()

        return digest


class LinkDigestRetrieveDeleteSerializer(serializers.ModelSerializer):
    topic = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='topic_name'
    )

    class Meta:
        model = LinkDigest
        fields = ['owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp']


# сериализатор для списка дайджестов сслыками
class LinkDigestListSerializer(serializers.ModelSerializer):
    topic = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='topic_name'
    )
    links = DigestLinksSerializer(many=True)

    class Meta:
        model = LinkDigest
        fields = ['id', 'owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp',
                  'links']


# сериализатор на получение картиночного дайджеста определнного пользователя
class UserImageDigestRetrieveSerializer(serializers.ModelSerializer):
    images = DigestImageCRDSerializer(many=True)

    class Meta:
        model = ImageDigest
        fields = ['id', 'owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp',
                  'images']


# сериализатор на получение ссылочного дайджеста определнного пользователя
class UserLinkDigestRetrieveSerializer(serializers.ModelSerializer):
    links = DigestLinksSerializer(many=True)

    class Meta:
        model = ImageDigest
        fields = ['id', 'owner', 'introduction', 'name', 'topic', 'conclusion', 'saves', 'public', 'created_timestamp',
                  'links']
