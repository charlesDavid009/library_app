from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import (RegisterUserSerializer, LoginSerializer)
from .models import MyUser
from rest_framework import generics
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model, login, logout


User = get_user_model()

ACTIONS = settings.ACTIONS



class RegisterUserPostView(generics.CreateAPIView):
    serializer_class        = RegisterUserSerializer
    queryset                = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = RegisterUserSerializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            res = {
                "user" : user.username,
                "user_id" : user.id,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_403_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        data= request.data
        serializer = LoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.data
            return Response(user, status=status.HTTP_200_OK)
        return Response (serializer.errors, status= status.HTTP_400_BAD_REQUEST)
