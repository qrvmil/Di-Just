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


# TODO: list of digests
# TODO: add pagination


class DigestImagesUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsOwner]
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageUpdateSerializer


class DigestImagesRetrieveDeleteAPI(generics.RetrieveDestroyAPIView):
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageCRDSerializer


class DigestImageCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageCRDSerializer


class ImageDigestCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ImageDigest.objects.all()
    serializer_class = ImageDigestCreateSerializer


class ImageDigestUpdateAPI(APIView):
    permission_classes = [IsOwner]

    # TODO make subscription
    def put(self, request, pk):
        data = request.data
        topics = []
        if "topic" in data.keys():
            topics = data.pop("topic")

        if "updates" in data.keys():
            updates = json.loads(data["updates"])["updates"]

            if "pictures" in data.keys():
                pictures = data.pop("pictures")
            else:
                pictures = []

            for elem in updates:
                try:
                    instance = DigestImages.objects.get(pk=elem["pk"])
                except:
                    return Response({"error": "invalid image pk"})

                if instance.owner != request.user.profile:  # IsOwner check
                    return Response({"Allowed only for owners"})

                if elem["type"] == "picture":
                    storage, path = instance.picture.storage, instance.picture.path
                    storage.delete(path)

                    try:
                        instance.picture = pictures[elem["picture"]]
                    except KeyError:
                        return Response({"error": "no [picture] field in updates"})
                    except IndexError:
                        return Response({"error": "invalid index for picture in picture array"})
                    instance.save()

                else:
                    instance.description = elem['description']
                    instance.save()

        try:
            digest = ImageDigest.objects.get(pk=pk)
        except:
            return Response({"error": "invalid digest pk"})

        if digest.owner != request.user.profile:  # IsOwner check
            return Response({"Allowed only for owners"})

        digest.name = data.get("name", digest.name)
        digest.introduction = data.get("introduction", digest.introduction)
        digest.conclusion = data.get("conclusion", digest.conclusion)

        if topics:
            for topic in digest.topic.all():
                digest.topic.remove(topic)
            for topic in topics:
                digest.topic.add(topic)

        digest.save()

        return Response({"status": "successfully updated"})


class ImageDigestRetrieveAPI(APIView):

    def get(self, request, pk):
        try:
            digest = ImageDigest.objects.get(pk=pk)
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

    def put(self, request, pk):
        data = request.data

        topics = []
        if "topic" in data.keys():
            topics = data.pop("topic")

        if "updates" in request.data:
            updates = json.loads(data["updates"])["updates"]
            for update in updates:
                try:
                    link = DigestLinks.objects.get(pk=update["pk"])
                except:
                    return Response({"error": "Invalid link pk"})

                link.link = update.get("link", link.link)
                link.description = update.get("description", link.description)

                link.save()

        try:
            digest = LinkDigest.objects.get(pk=pk)
        except:
            return Response({"error": "invalid digest pk"})

        if digest.owner != request.user.profile:  # IsOwner check
            return Response({"Allowed only for owners"})

        digest.name = data.get("name", digest.name)
        digest.introduction = data.get("introduction", digest.introduction)
        digest.conclusion = data.get("conclusion", digest.conclusion)

        if topics:
            for topic in digest.topic.all():
                digest.topic.remove(topic)
            for topic in topics:
                digest.topic.add(topic)

        digest.save()

        return Response({"status": "successfully updated"})


class LinkDigestRetrieveAPI(APIView):

    def get(self, request, pk):
        try:
            digest = LinkDigest.objects.get(pk=pk)
        except:
            return Response({"error": "invalid pk"})

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

    def post(self, request):
        data = request.data
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

    def put(self, request, pk):
        comment = Comments.objects.get(pk=pk)
        if comment.user != request.user.profile:
            return Response({"allowed only for owner"})

        comment.text = request.data.get("text", comment.text)
        serializer = CommentSerializer(instance=comment)
        return Response({"updated": serializer.data})


class CommentDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsCommenter]
    queryset = Comments
    serializer_class = CommentSerializer


# NB ссылка вида http://127.0.0.1:8000/digest/comments/?pk=9&digest-type=img-digest
class DigestCommentsRetrieveAPI(APIView):

    def get(self, request):
        data = request.query_params
        if data["digest-type"] == "img-digest":
            comments = ImageDigest.objects.get(pk=int(data["pk"])).comments.all()
        else:
            comments = LinkDigest.ojects.get(pk=int(data["pk"])).comments.all()

        comments = CommentListSerializer(data=comments, many=True)
        comments.is_valid()

        return Response({"Comments": comments.data})


class UserDigestRetrieveAPI(APIView, PageNumberPagination):

    def get(self, request, pk):
        user = Profile.objects.get(pk=pk)
        if request.user.profile != user:
            img_digests = user.created_img_digest.filter(public=True)
            link_digests = user.created_link_digest.filter(public=True)
        else:
            img_digests = user.created_img_digest.all()
            link_digests = user.created_link_digest.all()

        img_digests = UserImageDigestRetrieveSerializer(data=img_digests, many=True)
        link_digests = UserLinkDigestRetrieveSerializer(data=link_digests, many=True)

        img_digests.is_valid()
        link_digests.is_valid()

        return Response({"image digests": img_digests.data, "link digests": link_digests.data})


class DigestSaveAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pk = request.data["pk"]
        digest_type = request.data["digest-type"]
        if digest_type == 'img-digest':
            digest = ImageDigest.objects.get(pk=pk)
        else:
            digest = LinkDigest.objects.get(pk=pk)

        digest.saves.add(request.user.profile)

        return Response({"successfully saved"})


class SavedImageDigestsAPI(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
        paginator = CustomPagination()
        user = request.user.profile
        saved_img_digests = user.saved_img_digest.all()
        result_page = paginator.paginate_queryset(saved_img_digests, request)
        saved_img_digest = UserImageDigestRetrieveSerializer(data=result_page, many=True)
        saved_img_digest.is_valid()
        all = saved_img_digest.data

        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class SavedLinkDigestsAPI(APIView):
    permission_classes = [IsOwner]

    def get(self, request):
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

    def get(self, request):
        data = request.data
        paginator = CustomPagination()
        if "topics" in data.keys():
            topics = tuple(data["topics"])

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT DISTINCT imagedigest_id FROM digest_imagedigest_topic WHERE topics_id IN {topics}")
                row = [i[0] for i in cursor.fetchall()]
                img_digests = ImageDigest.objects.filter(id__in=row, public=True)

        elif "owner" in data.keys():
            owner = data["owner"]
            img_digests = ImageDigest.objects.filter(owner__user__username=owner, public=True)

        elif "time" in data.keys():
            if data["time"] == "new":
                img_digests = ImageDigest.objects.filter(public=True).order_by('-created_timestamp').all()
            elif data["time"] == "old":
                img_digests = ImageDigest.objects.filter(public=True).order_by('created_timestamp').all()

        result_page_1 = paginator.paginate_queryset(img_digests, request)
        img_digests = ImageDigestListSerializer(result_page_1, many=True)
        all = img_digests.data

        response = CustomPagination.get_paginated_response(paginator, all)
        return response


class LinkDigestListAPI(APIView):

    def get(self, request):
        data = request.data
        paginator = CustomPagination()
        if "topics" in data.keys():
            topics = tuple(data["topics"])

            with connection.cursor() as cursor:
                cursor.execute(
                    f"SELECT DISTINCT linkdigest_id FROM digest_linkdigest_topic WHERE topics_id IN {topics}")
                row = [i[0] for i in cursor.fetchall()]
                link_digests = LinkDigest.objects.filter(id__in=row, public=True)

        elif "owner" in data.keys():
            owner = data["owner"]
            link_digests = LinkDigest.objects.filter(owner__user__username=owner, public=True)

        elif "time" in data.keys():
            if data["time"] == "new":
                link_digests = LinkDigest.objects.filter(public=True).order_by('-created_timestamp').all()
            elif data["time"] == "old":
                link_digests = LinkDigest.objects.filter(public=True).order_by('created_timestamp').all()

        result_page_1 = paginator.paginate_queryset(link_digests, request)
        link_digests = ImageDigestListSerializer(result_page_1, many=True)
        all = link_digests.data

        response = CustomPagination.get_paginated_response(paginator, all)
        return response
