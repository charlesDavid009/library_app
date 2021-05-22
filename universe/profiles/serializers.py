from rest_framework import serializers
from .models import Profile, Follow, profiles_followed
from django.conf import settings
from blog.models import Blog, Comment
from groups.models import Group, MyBlog, Message
from pages.models import Page, Blogs

ACTIONS = settings.ACTIONS


class ProfileSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)
    blogs = serializers.SerializerMethodField(read_only=True)
    groups = serializers.SerializerMethodField(read_only=True)
    pages = serializers.SerializerMethodField(read_only=True)
    replies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = '__all__'

    def get_followers(self, obj):
        return obj.followers.count()
    
    def get_following(self, obj):
        return obj.following.count()

    def get_blogs(self, obj):
        user = obj.user
        qs= Blog.objects.filter(user = user)
        blog_lists = int(qs.count())
        vd = MyBlog.objects.filter(owner = user)
        myblog = int(vd.count())
        vq = Blogs.objects.filter(user = user)
        blog = int(vq.count())
        blogs = blog_lists + myblog + blog
        return blogs

    def get_groups(self, obj):
        user = obj.user
        qs= Group.objects.filter(owner = user)
        blog_lists = qs.count()
        return blog_lists

    def get_pages(self, obj):
        user = obj.user
        qs= Page.objects.filter(users = user)
        blog_lists = qs.count()
        return blog_lists

    def get_replies(self, obj):
        user = obj.user
        qs= Comment.objects.filter(user = user)
        blog_lists = int(qs.count())
        vd = Message.objects.filter(owner = user)
        myblog = int(vd.count())
        blogs = blog_lists + myblog
        return blogs
        

class CreateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=False)
    middle_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    bio = serializers.CharField(required=False)
    picture = serializers.ImageField(required=False)
    dob = serializers.IntegerField(required=False)
    contact = serializers.IntegerField(required=False)
    nationality = serializers.CharField(max_length=250, required=False)

    def create(self, validated_data):
        return Profile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.middle_name = validated_data.get(
            'middle_name', instance.middle_name)
        instance.bio = validated_data.get('bio ', instance.bio)
        instance.email = validated_data.get('email ', instance.email)
        instance.contact = validated_data.get('contact', instance.contact)
        instance.nationality = validated_data.get(
            'nationality ', instance.nationality)
        instance.save()
        return instance


class ActionProfileSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if value in ACTIONS:
            return value
        return serializers.ValidationError(status=400)


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'


class MyFollowingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = profiles_followed
        fields = '__all__'
