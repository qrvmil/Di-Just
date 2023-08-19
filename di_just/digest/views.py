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


# TODO: topics
# TODO: subscription
# TODO: get digest comments
# TODO: list of digests
# TODO: sorter
# TODO: list of profiles
# TODO: get users' digests
# TODO: add comments to digest.get
# TODO: add pagination
# TODO: test API


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
                    return Response({"error": "invalid pk"})

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
            return Response({"error": "invalid pk"})

        if digest.owner != request.user.profile:  # IsOwner check
            return Response({"Allowed only for owners"})

        digest.name = data.get("name", digest.name)
        digest.introduction = data.get("introduction", digest.introduction)
        digest.conclusion = data.get("conclusion", digest.conclusion)

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
        if digest.user != request.user.profile:  # IsOwner check
            return Response({"Allowed only for owners"})
        digest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class LinkDigestCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = LinkDigest
    serializer_class = LinkDigestCreateSerializer


class LinkDigestUpdateAPI(APIView):

    def put(self, request, pk):
        data = request.data
        if "updates" in request.data:
            updates = json.loads(data["updates"])["updates"]
            for update in updates:
                try:
                    link = DigestLinks.objects.get(pk=update["pk"])
                except:
                    return Response({"error": "Invalid pk"})

                link.link = update.get("link", link.link)
                link.description = update.get("description", link.description)

                link.save()



        try:
            digest = LinkDigest.objects.get(pk=pk)
        except:
            return Response({"error": "invalid pk"})

        if digest.owner != request.user.profile:  # IsOwner check
            return Response({"Allowed only for owners"})

        digest.name = data.get("name", digest.name)
        digest.introduction = data.get("introduction", digest.introduction)
        digest.conclusion = data.get("conclusion", digest.conclusion)

        digest.save()

        return Response({"status": "successfully updated"})




class TopicAPI():
    pass
