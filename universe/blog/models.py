from __future__ import unicode_literals
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from taggit.managers import TaggableManager
from .managers import BlogManager, DraftManager, PublishManager
from django.utils.text import slugify
from django.db.models.signals import pre_save
from markdown_deux import markdown
from .utils import get_read_time

# Create your models here.\
USER = get_user_model()


class Blog(models.Model):
    status = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )
    """
    API FOR USER TO CREATE THEIR OWN BLOG POST
    """
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(unique = True)
    title = models.CharField(max_length=200, blank=False, null=True)
    content = models.CharField(max_length=8000, blank=False, null=True)
    picture = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Blog_comments', blank=True, through='Comment')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Blog_likes', blank=True, through='BlogLikes')
    reports = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='Blog_reports', blank=True, through='Report')
    read_time = models.TimeField(null= True, blank= True)
    status = models.CharField(max_length = 100, choices = status, default = 'draft')
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)

    objects = BlogManager()
    drafts   = DraftManager()
    publish = PublishManager()

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse("blog:-:detail", kwargs={"pk": self.id})

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return markdown_text

    @property
    def is_reblog(self):
        return self.parrent != None

    @property
    def owner(self):
        return self.user

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Blog.objects.filter(slug=slug).order_by('-id')
    qs2 = Blog.drafts.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = "%s-%s" %(slug,  qs.first().id)
        return create_slug(instance, new_slug= new_slug)
    if qs2.exists():
        new_slug = "%s-%s" %(slug,  qs2.first().id)
        return create_slug(instance, new_slug= new_slug)
    return slug

def pre_save_blog_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_blog_reciever, sender = Blog)

class Report(models.Model):
    """
    GETS THE TIME LIKES HAPPENED
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class BlogLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Comment(models.Model):
    """
    MODELS FOR COMMENTS 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(USER, blank=True, related_name='Commnets_likes', through="CommentLikes")
    comment = models.ManyToManyField(USER, blank=True,  related_name='Commnets_count', through="SubComment")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    @property
    def user_info(self):
        return self.user


class CommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class SubComment(models.Model):
    """
    MODELS FOR SUB_COMMENTS
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(
        USER, blank=True, related_name='SubCommnets_likes', through="SubCommentLikes")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("subcomment_threads", kwargs={"id": self.id})

    @property
    def user_info(self):
        return self.user


class SubCommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(SubComment, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
