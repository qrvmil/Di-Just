from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from user.models import Profile
from django.contrib.auth.models import User
from user.serializers import ProfileSerializer, UserRegisterSerializer


class RegisterUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)

#
# @csrf_exempt
# def profiles_list(request):
#     """
#     List all code profiles, or create a new profile.
#     """
#     if request.method == 'GET':
#         profiles = Profile.objects.all()
#         serializer = ProfileSerializer(profiles, many=True)
#         # print(serializer.data)
#         return JsonResponse(serializer.data, safe=False)
#
#
# @csrf_exempt
# def profile_detail(request, pk):
#     """
#     Retrieve, update or delete a profile.
#     """
#     try:
#         profile = Profile.objects.get(pk=pk)
#     except Profile.DoesNotExist:
#         return HttpResponse(status=404)
#
#     if request.method == 'GET':
#         serializer = ProfileSerializer(profile)
#         return JsonResponse(serializer.data)
#
#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = ProfileSerializer(profile, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)
#
#     elif request.method == 'DELETE':
#         profile.delete()
#         return HttpResponse(status=204)
