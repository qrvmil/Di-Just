from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from digest.models import ImageDigest, LinkDigest, DigestImages
from digest.serializers import *
from rest_framework import generics


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


class ImageDigestUpdateAPI(generics.UpdateAPIView):
    queryset = ImageDigest.objects.all()
    serializer_class = ImageDigestUpdateSerializer


class LinkDigestAPI():
    pass


class TopicAPI():
    pass
