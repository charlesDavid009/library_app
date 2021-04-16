from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from blog.models import Blog
from django.utils.text import slugify
from django.db.models.signals import pre_save
from markdown_deux import markdown
from django.conf import settings

# Create your models here.

USER = settings.AUTH_USER_MODEL

class ProfileQuerySet(models.QuerySet):
    def search(self, user, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(first_name__icontains=query) |
                Q(user__username__icontains=query) |
                Q(last_name_icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

    def following_feed(self, user):
        user = Profile.objects.filter(user = user)
        profiles_exist = user.following.exists()
        followed_users = []
        if profiles_exist:
            followed_users = user.following.values_list(
                "users__id", flat=True)
        return self.filter(user__id__in=followed_users).distinct().order_by("-created_at")

class ProfileManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return ProfileQuerySet(self.model, using=self._db)

    def following_feed(self, user):
        return self.get_queryset().following_feed(user)

    def search(self, user, query=None):
        qs = self.get_queryset().search(query=query)
        return qs
class Profile(models.Model):
    """
    This is the models for USER PROFILES
    """
    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True)
    bio = models.TextField(blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    dob = models.IntegerField(blank=True, null=True)
    contact = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    blogs = models.ManyToManyField(USER, related_name='blog_counts', blank=True, through="Blog_Lists")
    followers = models.ManyToManyField(USER, related_name='my_followings', blank=True,  through="Follow")
    following = models.ManyToManyField(USER, related_name='profile_follows', blank=True, through="profiles_followed")

    objects = ProfileManager()

    def user_did_save(sender, instance, created, *args, **kwargs):
        if created:
            Profile.objects.get_or_create(user=instance)

    post_save.connect(user_did_save, sender=USER)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.user)
    if new_slug is not None:
        slug = new_slug
    qs = Profile.objects.filter(slug=slug).order_by('-id')
    if qs.exists():
        new_slug = "%s-%s" %(slug,  qs.first().id)
        return create_slug(instance, new_slug= new_slug)
    return slug

def pre_save_profile_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_profile_reciever, sender = Profile)
class Follow(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    profiles = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class profiles_followed(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Blog_lists(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
