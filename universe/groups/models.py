from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from .managers import MyBlogManager, GroupManager

# Create your models here.

USER = get_user_model()


class Group(models.Model):
    """
    This is the models for USER PROFILES
    """
    group_name = models.CharField(max_length=100, blank=False, null=True)
    slug = models.SlugField(blank = True, null=  True, unique = True)
    users = models.ManyToManyField(USER, related_name='groups_users', blank=True, through="Uses")
    request = models.ManyToManyField(USER, related_name='groups_request', blank=True, through="Request")
    admin = models.ManyToManyField(USER, related_name='groups_admin', blank=True, through="Admins")
    description = models.TextField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    owner = models.ForeignKey(USER, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    follower = models.ManyToManyField(USER, related_name="followings", blank=True, through="Follows")
    
    objects = GroupManager()

    @property
    def group_info(self):
        return self.group_name


class Follows(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user

class Uses(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    members = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Admins(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    container = models.ForeignKey(Group, related_name="my_admin",  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Request(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="my_group",  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class MyBlog(models.Model):
    """
    This is the models for items
    """
    parent = models.ForeignKey("self", null=True, blank=True,  on_delete=models.SET_NULL)
    reference = models.ForeignKey(Group, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False, null=True)
    slug = models.SlugField(blank = True, null=  True, unique = True)
    content = models.TextField(blank=False, null=True)
    picture = models.ImageField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(USER, related_name='Blog_owner', blank=True,  through="MyBlogLikes")
    comment = models.ManyToManyField(USER, related_name="owners", blank=True, through="Message")
    report = models.ManyToManyField(USER, related_name="reported", blank=True, through="Reports")
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MyBlogManager()

    class Meta:
        ordering = ['-created_at']

    @property
    def owner_info(self):
        return self.owner

    @property
    def is_reblog(self):
        return self.parent != None


class MyBlogLikes(models.Model):
    users = models.ForeignKey(USER, on_delete=models.CASCADE)
    blog = models.ForeignKey(MyBlog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Reports(models.Model):
    users = models.ForeignKey(USER, on_delete=models.CASCADE)
    blog = models.ForeignKey(MyBlog, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Message(models.Model):
    reference = models.ForeignKey(MyBlog, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    like = models.ManyToManyField(USER, related_name='blog_message', blank=True, through="MessageLikes")
    created_at = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField(USER, related_name='Message_owner', blank=True, through="MyComment")

    class Meta:
        ordering = ["-created_at"]

    @property
    def owner_info(self):
        return self.owner


class MessageLikes(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    post = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class MyComment(models.Model):
    reference = models.ForeignKey(Message, on_delete=models.CASCADE)
    owners = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    like = models.ManyToManyField(USER, related_name='message_owner', blank=True, through="CommentsLikes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    @property
    def owner_info(self):
        return self.owner


class CommentsLikes(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    post = models.ForeignKey(MyComment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
