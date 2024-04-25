from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from digest.custom_permissions import *
from digest.models import ImageDigest, LinkDigest, DigestImages
from digest.serializers import *
from rest_framework import generics, status
import json
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from digest.pagination import CustomPagination


# обновление картнинок дайджеста
class DigestImagesUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageUpdateSerializer


# получаение/удаление картинок дайджеста
class DigestImagesRetrieveDeleteAPI(generics.RetrieveDestroyAPIView):
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageCRDSerializer


# создание картинки дайджеста
class DigestImageCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageCRDSerializer


# создание дайджеста с картинками
class ImageDigestCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ImageDigest.objects.all()
    serializer_class = ImageDigestCreateSerializer


# обновление дайджеста с картинками
class ImageDigestUpdateAPI(APIView):
    permission_classes = [IsOwner]

    # данная функция обрабатывает запрос на обновление дайджеста
    # request -- данные с клиента
    def put(self, request, pk):

        data = request.data
        topics = []
        # получение всех тегов дайджеста
        if "topic" in data.keys():
            topics = data.pop("topic")

        try:
            digest = ImageDigest.objects.get(pk=pk)
        except:
            return Response({"error": "invalid digest pk"})

        # получаение всех обновлений
        if "updates" in data.keys():
            updates = json.loads(data["updates"])["updates"]

            if "pictures" in data.keys():
                pictures = data.pop("pictures")
            else:
                pictures = []

            for elem in updates:
                if elem['pk'] < 0:
                    img = DigestImages.objects.create(digest=digest, picture=pictures[elem["picture"]],
                                                      description="No description")
                else:
                    instance = DigestImages.objects.get(pk=elem["pk"])

                    if instance.digest.owner.id != request.user.id:  # IsOwner check
                        return Response({"Allowed only for owners"})

                    if elem["type"] == "picture":
                        storage, path = instance.picture.storage, instance.picture.path
                        storage.delete(path)

                        try:
                            instance.picture = pictures[elem["picture"]]
                        # обработка ошибок, если в запросе не хватает массива с картинками или некорректный
                        # индекс в массиве на обновлние картинок
                        except KeyError:
                            return Response({"error": "no [picture] field in updates"})
                        except IndexError:
                            return Response({"error": "invalid index for picture in picture array"})
                        instance.save()

                    else:
                        instance.description = elem['description']
                        instance.save()

        # try:
        #     digest = ImageDigest.objects.get(pk=pk)
        #
        # except:
        #     return Response({"error": "invalid digest pk"})
        print('-----', digest.owner.id, request.user.id)
        if digest.owner.id != request.user.id:  # IsOwner check
            return Response({"Allowed only for owners"})
        # обновлние основной информации дайджеста
        digest.name = data.get("name", digest.name)
        digest.introduction = data.get("introduction", digest.introduction)
        digest.conclusion = data.get("conclusion", digest.conclusion)
        digest.public = data.get("public", digest.public)
        # проверка на обновление тегов
        if topics:
            for topic in digest.topic.all():
                digest.topic.remove(topic)
            for topic in topics:
                digest.topic.add(topic)

        digest.save()

        return Response({"status": "successfully updated"})


class ImageDigestRetrieveAPI(APIView):
    # обрабытывается запрос на получение дайджеста с картинками
    def get(self, request, pk):
        try:
            digest = ImageDigest.objects.get(pk=pk)
        # ошибка, если неверный id дайджеста
        except:
            return Response({"error": "invalid pk"})

        if not digest.public and (request.user != digest.owner.user):
            return Response({"error": "this digest is private"})

        images = DigestImages.objects.filter(digest=digest)
        images = DigestImageCRDSerializer(data=images, many=True)
        images.is_valid()
        digest = ImageDigestRetrieveDeleteSerializer(digest)

        return Response({"general info": digest.data, "digest images": images.data})


class ImageDigestDeleteAPI(APIView):
    # удаление дайджеста картинок
    # прописывается отдельно, так как необходимо удалить еще и саму картинку из хранилища на сервере
    def delete(self, request, pk):
        digest = ImageDigest.objects.get(pk=pk)
        if digest.owner != request.user.profile:  # IsOwner check
            return Response({"Allowed only for owners"})
        digest.delete()
        return Response({"successfully deleted"})


class LinkDigestCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LinkDigest
    serializer_class = LinkDigestCreateSerializer


class LinkDigestUpdateAPI(APIView):
    # ообновление дайджеста ссылками
    def put(self, request, pk):
        data = request.data

        digest = LinkDigest.objects.get(pk=pk)

        topics = []
        # проврка на наличие обновленных тегов
        if "topic" in data.keys():
            topics = data.pop("topic")
        # обновление ссылок и описаний к ним
        if "updates" in request.data:
            updates = json.loads(data["updates"])["updates"]
            for update in updates:

                if update["pk"] < 0:
                    new_link = DigestLinks.objects.create(digest=digest, link=update["link"],
                                                          description="No description")
                else:
                    link = DigestLinks.objects.get(pk=update["pk"])

                    link.link = update.get("link", link.link)
                    link.description = update.get("description", link.description)

                    link.save()

        if digest.owner != request.user.profile:  # IsOwner check
            return Response({"Allowed only for owners"})

        # обновление основной информации
        digest.name = data.get("name", digest.name)
        digest.introduction = data.get("introduction", digest.introduction)
        digest.conclusion = data.get("conclusion", digest.conclusion)
        digest.public = data.get("public", digest.public)

        # обновление тегов
        if topics:
            for topic in digest.topic.all():
                digest.topic.remove(topic)
            for topic in topics:
                digest.topic.add(topic)

        digest.save()

        return Response({"status": "successfully updated"})


class LinkDigestRetrieveAPI(APIView):
    # получение дайджеста ссылкой
    def get(self, request, pk):
        try:
            digest = LinkDigest.objects.get(pk=pk)
        except:
            return Response({"error": "invalid pk"})
        # проверка на то, что дайджест не приватный
        if not digest.public and (request.user != digest.owner.user):
            return Response({"error": "this digest is private"})

        links = DigestLinks.objects.filter(digest=digest)
        links = DigestLinksSerializer(data=links, many=True)
        links.is_valid()
        digest = LinkDigestRetrieveDeleteSerializer(digest)

        return Response({"general info": digest.data, "digest links": links.data})


class LinkDigestDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsOwner]
    queryset = LinkDigest
    serializer_class = LinkDigestRetrieveDeleteSerializer


class CommentCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    # создание коментария
    # request -- данные с клиента
    def post(self, request):
        data = request.data
        # проверка на то, что не указано сразу два вида дайджестов
        if "link_digest" in data.keys() and "img_digest" in data.keys():
            return Response({"error": "you can add comment only to one digest"})

        if not ("link_digest" in data.keys()) and not ("img_digest" in data.keys()):
            return Response({"error": "digest field is required"})
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"post": serializer.data})


class CommentUpdateAPI(APIView):
    permission_classes = [IsCommenter]

    # обновление комментария
    def put(self, request, pk):
        comment = Comments.objects.get(pk=pk)
        if comment.user != request.user.profile:
            return Response({"allowed only for owner"})

        comment.text = request.data.get("text", comment.text)
        serializer = CommentSerializer(instance=comment)
        return Response({"updated": serializer.data})


#
class CommentDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsCommenter]
    queryset = Comments
    serializer_class = CommentSerializer


# NB ссылка вида http://127.0.0.1:8000/digest/comments/?pk=9&digest-type=img-digest
class DigestCommentsRetrieveAPI(APIView):

    # получение всех комментарией к дайджесту
    def get(self, request):
        data = request.query_params
        paginator = CustomPagination()
        if data["type"] == "img":
            comments = ImageDigest.objects.get(pk=int(data["pk"])).comments.all()
        else:
            comments = LinkDigest.objects.get(pk=int(data["pk"])).comments.all()
        result_page = paginator.paginate_queryset(comments, request)
        comments = CommentListSerializer(data=result_page, many=True)
        comments.is_valid()
        all = comments.data

        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class UserImageDigestRetrieveAPI(APIView, PageNumberPagination):
    # для того, чтобы получить список созданных пользователем дайджестов,
    # прописывем отдельную функция на запрос get, которая добавялет пагинацию
    def get(self, request, pk):
        user = Profile.objects.get(pk=pk)
        # подключаем пагинацию
        paginator = CustomPagination()
        if request.user.profile != user:
            img_digests = user.created_img_digest.filter(public=True)
        else:
            img_digests = user.created_img_digest.all()
        result_page = paginator.paginate_queryset(img_digests, request)
        img_digests = UserImageDigestRetrieveSerializer(data=result_page, many=True)

        img_digests.is_valid()
        all = img_digests.data
        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class UserLinkDigestRetrieveAPI(APIView, PageNumberPagination):
    # аналогична функция на получения данных с пагинацией
    def get(self, request, pk):
        user = Profile.objects.get(pk=pk)
        paginator = CustomPagination()
        if request.user.profile != user:
            link_digests = user.created_link_digest.filter(public=True)
        else:
            link_digests = user.created_link_digest.all()
        result_page = paginator.paginate_queryset(link_digests, request)
        link_digests = UserLinkDigestRetrieveSerializer(data=result_page, many=True)

        link_digests.is_valid()
        all = link_digests.data
        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class DigestSaveAPI(APIView):
    permission_classes = [IsAuthenticated]

    # данная функция отвечает за обновление состояние дайджеста, то есть то что мы его сохранили
    # request -- запрос с клиента
    def post(self, request):
        pk = request.data["pk"]
        digest_type = request.data["digest-type"]
        if digest_type == 'img-digest':
            digest = ImageDigest.objects.get(pk=pk)
        else:
            digest = LinkDigest.objects.get(pk=pk)

        digest.saves.add(request.user.profile)

        return Response({"successfully saved"})


class DigestUnsaveAPI(APIView):
    permission_classes = [IsAuthenticated]

    # аналогичная функция для удаления дайджеста из сохраненных
    def post(self, request):
        pk = request.data["pk"]
        digest_type = request.data["digest-type"]
        if digest_type == 'img-digest':
            digest = ImageDigest.objects.get(pk=pk)
        else:
            digest = LinkDigest.objects.get(pk=pk)

        digest.saves.remove(request.user.profile)

        return Response({"successfully unsaved"})


class SavedImageDigestsAPI(APIView):
    permission_classes = [IsOwner]

    # получение всех сохраненных дайджестов картинками
    def get(self, request):
        # подключаем пагинацию
        paginator = CustomPagination()
        user = request.user.profile
        saved_img_digests = user.saved_img_digest.all()
        result_page = paginator.paginate_queryset(saved_img_digests, request)
        saved_img_digest = UserImageDigestRetrieveSerializer(data=result_page, many=True)
        saved_img_digest.is_valid()
        all = saved_img_digest.data
        # возвращаем запрос с пагинацией
        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class SavedLinkDigestsAPI(APIView):
    permission_classes = [IsOwner]

    # получение всех сохраненных дайджестов ссылками
    def get(self, request):
        # подключение пагинации
        paginator = CustomPagination()
        user = request.user.profile
        saved_link_digest = user.saved_link_digest.all()
        result_page = paginator.paginate_queryset(saved_link_digest, request)
        saved_link_digest = UserLinkDigestRetrieveSerializer(data=result_page, many=True)
        saved_link_digest.is_valid()

        all = saved_link_digest.data
        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class ImageDigestListAPI(APIView):
    # получение всех жайджестов с картинками и их сортировка
    def get(self, request):
        # проверка на то, какой именно запрос на сортирвку нам поступил
        data1 = request.query_params.getlist('topics[]', '')  # request.GET.dict() # request.data
        data2 = request.GET.get('owner', '')
        data3 = request.GET.get('time', '')

        if data1:
            data = {'topics': data1}
        elif data2:
            data = {'owner': data2}
        elif data3:
            data = {'time': data3}
        else:
            return Response({"failed"})
        # подключение пагинации
        paginator = CustomPagination()
        if "topics" in data.keys() and data['topics'] != []:
            topics = tuple(data["topics"])
            if len(topics) == 1:
                topics = f'({topics[0]})'

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT DISTINCT imagedigest_id FROM digest_imagedigest_topic WHERE topics_id IN {topics}")
                row = [i[0] for i in cursor.fetchall()]
                img_digests = ImageDigest.objects.filter(id__in=row, public=True)
        # проверка, что сортировка идет по создателю
        elif "owner" in data.keys():
            owner = data["owner"]
            # NB! Передается username пользователя!
            img_digests = ImageDigest.objects.filter(owner__user__username=owner, public=True)
        # проверка, что сортирвка идет по времени
        elif "time" in data.keys():
            if data["time"] == "new":
                img_digests = ImageDigest.objects.filter(public=True).order_by('-created_timestamp').all()
            elif data["time"] == "old":
                img_digests = ImageDigest.objects.filter(public=True).order_by('created_timestamp').all()
        # пагинация
        result_page_1 = paginator.paginate_queryset(img_digests, request)
        img_digests = ImageDigestListSerializer(result_page_1, many=True)
        all = img_digests.data
        # фомируем ответ с пагинацией
        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class LinkDigestListAPI(APIView):

    def get(self, request):
        # проверка на то, какой именно запрос на сортирвку нам поступил
        data1 = request.query_params.getlist('topics[]', '')  # request.GET.dict() # request.data
        data2 = request.GET.get('owner', '')
        data3 = request.GET.get('time', '')
        #
        if data1:
            data = {'topics': data1}
        elif data2:
            data = {'owner': data2}
        elif data3:
            data = {'time': data3}
        else:
            return Response({"failed"})
        # # подключение пагинации
        paginator = CustomPagination()
        #
        if "topics" in data.keys() and data['topics'] != []:
            topics = tuple(data["topics"])
            if len(topics) == 1:
                topics = f'({topics[0]})'

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT DISTINCT linkdigest_id FROM digest_linkdigest_topic WHERE topics_id IN {topics}")
                row = [i[0] for i in cursor.fetchall()]
                link_digests = LinkDigest.objects.filter(id__in=row, public=True)
        # проверка, что сортировка идет по создателю
        elif "owner" in data.keys():
            owner = data["owner"]
            link_digests = LinkDigest.objects.filter(owner__user__username=owner, public=True)
        # проверка, что сортирвка идет по времени
        elif "time" in data.keys():
            if data["time"] == "new":
                link_digests = LinkDigest.objects.filter(public=True).order_by('-created_timestamp').all()
            elif data["time"] == "old":
                link_digests = LinkDigest.objects.filter(public=True).order_by('created_timestamp').all()

        result_page_1 = paginator.paginate_queryset(link_digests, request)
        link_digests = LinkDigestListSerializer(result_page_1, many=True)
        all = link_digests.data
        # фомируем ответ с пагинацией
        response = CustomPagination.get_paginated_response(paginator, all)
        return response
