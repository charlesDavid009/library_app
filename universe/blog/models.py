from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from taggit.managers import TaggableManager
from .managers import BlogManager, DraftManager, PublishManager
from django.template.defaultfilters import slugify

USER = get_user_model()

# Create your models here.



class Blog(models.Model):
    status = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )
    """
    API FOR USER TO CREATE THEIR OWN BLOG POST
    """
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    slug = models.SlugField(blank = True, null=  True, unique = True)
    title = models.CharField(max_length=200, blank=False, null=True)
    content = models.CharField(max_length=8000, blank=False, null=True)
    picture = models.ImageField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.ManyToManyField(User, related_name='Blog_comments', blank=True, through='Comment')
    likes = models.ManyToManyField(User, related_name='Blog_likes', blank=True, through='BlogLikes')
    reports = models.ManyToManyField(User, related_name='Blog_reports', blank=True, through='Report')
    #published = models.DateTimeField(default = timezone.now())
    status = models.CharField(max_length = 100, choices = status, default = 'draft')
    tags = TaggableManager()
    created = models.DateTimeField(auto_now_add=True)

    objects = BlogManager()
    drafts   = DraftManager()
    publish = PublishManager()

    class Meta:
        ordering = ['-id']

    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"pk": self.pk})

    @property
    def is_reblog(self):
        return self.parrent != None

    @property
    def owner(self):
        return self.user.username


class Report(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class BlogLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class Comment(models.Model):
    """
    MODELS FOR COMMENTS 
    """
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(USER, blank=True, related_name='Commnets_likes', through="CommentLikes")
    comment = models.ManyToManyField(USER, blank=True,  related_name='Commnets_count', through="SubComment")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    @property
    def user_info(self):
        return self.user

    #def get_absolute_url(self):
        #return reverse("model_detail", kwargs={"pk": self.pk})
    


class CommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user


class SubComment(models.Model):
    """
    MODELS FOR SUB_COMMENTS
    """
    blog = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    text = models.TextField()
    like = models.ManyToManyField(
        USER, blank=True, related_name='SubCommnets_likes', through="SubCommentLikes")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("subcomment_threads", kwargs={"pk": self.pk})

    @property
    def user_info(self):
        return self.user


class SubCommentLikes(models.Model):
    """
    GETS THE TIME LIKES HAPPENED 
    """
    blog = models.ForeignKey(SubComment, on_delete=models.CASCADE)
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def user_info(self):
        return self.user
