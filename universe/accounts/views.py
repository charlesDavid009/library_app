from django.shortcuts import render
from django.shortcuts import render
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from django.contrib import auth
import jwt

from .models import User
from .serializer import RegisterSerializer, UserSerializer, LoginSerializer

ACTIONS = settings.ACTIONS

# Create your views here.

class RegisterUserPostView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data = self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginUserPostView(generics.CreateAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        attr = ('@')

        serializer = LoginSerializer(data = self.request.data)
        if serializer.is_valid():
            data =  serializer.validated_data
            username =  attr + data.get('username', '')
            print(username)
            password = data.get('password', '')
            print(password)
            user = auth.authenticate(username=username, password=password)
            payload = {'username': user.username}

            if user:
                auth_token = jwt.encode(
                    payload, settings.JWT_SECRET_KEY
                )

                serializer = UserSerializer(user)

                data = {
                    'user': serializer.data,
                    'token': auth_token
                }
                return Response(data, status=status.HTTP_200_OK)

            return Response({'details': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORISED)
