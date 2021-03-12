from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User
from .managers import PageManager, BlogsManager

User = get_user_model()
# Create your models here.

class Page(models.Model):
    users = models.ForeignKey(User,  on_delete=models.CASCADE)
    name = models.CharField(max_length = 400, blank = False, null = True)
    description = models.TextField(blank = True, null = True)
    slug = models.SlugField(blank = True, null=  True, unique = True)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)
    photo = models. ImageField(blank= True, null = True)
    followed = models.ManyToManyField(User, related_name = "followered", blank = True, through= 'Following')
    likes = models.ManyToManyField(User, related_name = "liked", blank= True, through = 'Liking')

    objects = PageManager()

class Following(models.Model):
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    references = models.ForeignKey(Page,  on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

class Liking(models.Model):
    uses = models.ForeignKey(User, on_delete=models.CASCADE)
    referenced = models.ForeignKey(Page,  on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)

class Blogs(models.Model):
    """
    API FOR USER TO CREATE THEIR OWN BLOG POST
    """
    reference = models.ForeignKey(Page, on_delete= models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200, blank=True, null=True)
    content = models.CharField(max_length=8000, blank=False, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    picture = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commented = models.ManyToManyField(User, related_name='page_comments', blank=True, through='Comments')
    likes = models.ManyToManyField(User, related_name='pasge_likes', blank=True, through='BlogLiked')
    created = models.DateTimeField(auto_now_add=True)

    objects = BlogsManager()
    class Meta:
        ordering = ['-id']

    @property
    def is_reblog(self):
        return self.parrent != None

    @property
    def owner(self):
        return self.user


class BlogLiked(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Comments(models.Model):
    """
    MODELS FOR COMMENTS 
    """
    blog = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(User, blank=True, related_name='Comments_likes', through="CommentLiked")
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class CommentLiked(models.Model):
    """
    GETS THE TIME LIKES HAPPENED
    """
    blog = models.ForeignKey(Comments, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
