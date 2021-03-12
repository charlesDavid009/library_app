from django.shortcuts import render
from .serializers import (
    ProfileSerializer,
    CreateProfileSerializer,
    ActionProfileSerializer,
    FollowSerializer)
from .models import Profile, Follow
from rest_framework import generics, mixins
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from rest_framework import status
from django.db.models import Q
from rest_framework.response import Response

ACTIONS = settings.ACTIONS

# Create your views here.

class CraeteProfileView(generics.CreateAPIView):
    """
    Create your Profile
    """
    serializer_class    = CreateProfileSerializer
    permission_classes  = [IsAuthenticated]

    def get_queryset(self):
        Profile.objects.all()

    def perform_create(self, serializer):
        serializer.save(user =self.request.user)

class UpdateProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Updates and Delete Uses Profiles
    """
    lookup                      = 'pk'
    serializer_class            = ProfileSerializer
    permission_classes          = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        qs = Profile.objects.all()
        return qs

class MyProfileView(generics.ListAPIView):
    """
    Gets Users Profile
    """
    serializer_class            = ProfileSerializer
    permission_classes          = [IsAuthenticated]

    def get_queryset(self):
        users = self.request.user
        qs = Profile.objects.filter(user = users)
        return qs

class GetUserView(generics.ListAPIView):
    """
    Search And Displays Profiles According to User Id Provided
    """
    serializer_class            = ProfileSerializer
    permission_classes          = [IsAuthenticated]

    def get_queryset(self):
        qs = Profile.objects.all()
        return qs


class UsersFollowersView(generics.ListAPIView):
    """
    DIsplays User Followers
    """
    lookup                     = 'id'
    serializer_class           = FollowSerializer
    permission_classes         = [IsAuthenticated]

    def get_queryset(self):
        user = self.kwargs.get('id')
        qs = Follow.objects.filter(profiles = user)
        return qs

class UserFollowingView(generics.ListAPIView):
    """
    Displays Users Followings
    """
    lookup                     = 'id'
    serializer_class           = FollowSerializer
    permission_classes         = [IsAuthenticated]

    def get_queryset(self):
        users = self.kwargs.get('id')
        obj = Follow.objects.filter(users__id = users)
        return obj

class ProfileActionView(generics.CreateAPIView):
    """
    Performs Action on Profiles
    """
    queryset                    = Profile.objects.all()
    serializer_class            = ActionProfileSerializer
    permission_classes          = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ActionProfileSerializer(data=request.data)
        me = request.user
        if serializer.is_valid():
            data = serializer.validated_data
            profile = data.get("id")
            action = data.get("action")
            qs = self.queryset.filter(user__id = profile)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if me != obj.user:
                if action == "follow":
                    obj.followers.add(me)
                    serializer = ProfileSerializer(obj)
                    return Response(serializer.data)
                elif action == "unfollow":
                    obj.followers.remove(me)
                    serializer = ProfileSerializer(obj)
                    return Response(serializer.data)
            serializer = ProfileSerializer(obj)
            return Response(serializer.data)

