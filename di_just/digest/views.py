from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from digest.models import ImageDigest, LinkDigest
from digest.serializers import ImageDigestSerializer, LinkDigestSerializer


@csrf_exempt
def img_digest_list(request):
    """
    List all code profiles, or create a new profile.
    """
    if request.method == 'GET':
        profiles = ImageDigest.objects.all()
        serializer = ImageDigestSerializer(profiles, many=True)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ImageDigestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def link_digest_list(request):
    """
    List all code profiles, or create a new profile.
    """
    if request.method == 'GET':
        profiles = LinkDigest.objects.all()
        serializer = LinkDigestSerializer(profiles, many=True)
        # print(serializer.data)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = LinkDigestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
