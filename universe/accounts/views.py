from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import (RegisterUserSerializer, LoginSerializer)
from .models import MyUser
from rest_framework import generics
from django.conf import settings
from django.db.models import Q


ACTIONS = settings.ACTIONS


class RegisterUserPostView(generics.CreateAPIView):
    serializer_class        = RegisterUserSerializer

    def get_queryset(self):
        return MyUser.objects.all()

    def perform_create(self, serializer):
        serializer.save()

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data= request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response (serializer.errors, status= status.HTTP_400_BAD_REQUEST)
