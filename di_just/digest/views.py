from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from digest.models import ImageDigest, LinkDigest, DigestImages
from digest.serializers import *
from rest_framework import generics, status
import json
import digest.models


# TODO: прописать permission на private дайджесты (разобраться как)
# TODO: сделать в начале класса проверку на поле is_privat и если true, то вставить кастомный IsOwner


class DigestImagesUpdateAPI(generics.UpdateAPIView):
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageUpdateSerializer


class DigestImagesRetrieveDeleteAPI(generics.RetrieveDestroyAPIView):
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageCRDSerializer


class DigestImageCreateAPI(generics.CreateAPIView):
    queryset = DigestImages.objects.all()
    serializer_class = DigestImageCRDSerializer


class ImageDigestCreateAPI(generics.CreateAPIView):
    queryset = ImageDigest.objects.all()
    serializer_class = ImageDigestCreateSerializer


class ImageDigestUpdateAPI(APIView):
    # TODO make subscription
    # TODO make validation
    def put(self, request, pk):
        data = request.data

        if "updates" in data.keys():
            updates = json.loads(data["updates"])["updates"]

            if "pictures" in data.keys():
                pictures = data.pop("pictures")
            else:
                pictures = []

            for elem in updates:  # TODO: добавить проверку вводимых данных
                try:
                    instance = DigestImages.objects.get(pk=elem["pk"])
                except:  # TO DO: посмотреть какая конкретно ошибка
                    return Response({"error": "invalid pk"})

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
        digest["name"] = data.get("name", digest["name"])
        digest["introduction"] = data.get("introduction", digest["introduction"])
        digest["conclusion"] = data.get("conclusion", digest["conclusion"])

        digest.save()

        return Response({"status": "successfully updated"})


class ImageDigestRetrieveDeleteAPI(APIView):

    def get(self, request, pk):
        try:
            digest = ImageDigest.objects.get(pk=pk)
        except:
            return Response({"error": "invalid pk"})
        images = DigestImages.objects.filter(digest=digest)
        images = DigestImageCRDSerializer(data=images, many=True)
        images.is_valid()
        digest = ImageDigestRetrieveDeleteSerializer(digest)

        return Response({"general info": digest.data, "digest images": images.data})

    def delete(self, request, pk):
        digest = ImageDigest.objects.get(pk=pk)
        digest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LinkDigestAPI():
    pass


class TopicAPI():
    pass
