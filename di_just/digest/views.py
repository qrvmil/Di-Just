from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from digest.models import ImageDigest, LinkDigest, DigestImages
from digest.serializers import *
from rest_framework import generics
import json
import digest.models


# TO DO: прописать permission на private дайджесты (разобраться как)
# сделать в начале класса проверку на поле is_privat и если true, то вставить кастомный IsOwner


class DigestImagesUpdateAPI(generics.UpdateAPIView):
    # TO DO прописать апдейт (через сериализатор) и delete (через сериализатор) для картинок
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
    # TO DO make subscription
    def put(self, request, pk):
        data = request.data
        if "updates" in data.keys():
            updates = json.loads(data["updates"])["updates"]
            if "pictures" in data.keys():
                pictures = data.pop("pictures")
            else:
                pictures = []
            for elem in updates:  # TO DO: добавить проверку вводимых данных
                try:
                    instance = DigestImages.objects.get(pk=elem["pk"])
                except:
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
        except: # TO DO посмотреть какая тут конкретно возвращается ошибка
            return
        digest["name"] = data.get("name", digest["name"])
        digest["introduction"] = data.get("introduction", digest["introduction"])
        digest["conclusion"] = data.get("conclusion", digest["conclusion"])

        digest.save()

        return Response({"status": "success"})


class LinkDigestAPI():
    pass


class TopicAPI():
    pass
