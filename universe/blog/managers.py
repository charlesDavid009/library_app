from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from taggit.managers import TaggableManager

USER = get_user_model()

class BlogQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug_icontains=query))
            qs = qs.filter(or_lookup)
            qs = qs.filter(status = 'publish').distinct()
        return qs

    def feed(self, user):
        profiles_exist = user.my_followings.exists()
        followed_users = []
        if profiles_exist:
            followed_users = user.my_followings.values_list("user__id", flat=True)
        return self.filter(
            Q(user__id__in=followed_users) |
            Q(user=user)
        ).distinct().order_by("-created")

class BlogManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BlogQuerySet(self.model, using=self._db)

    def feed(self, user):
        return self.get_queryset().feed(user).filter(status = 'publish')

    def search(self, user, query= None):
        qs  = self.get_queryset().search(query=query)
        return qs.feed(user)



class DraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status= 'draft')


class PublishManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset().filter(status='publish')


class PostQueryset(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains = query) |
                Q(content__icontains = query) |
                Q(slug_icontains = query)
            )
            qs = qs.filter(or_lookup)
            qs = qs.filter(status = 'publish').distinct()
        return qs

class PostManager(models.Manager):
    def get_queryset(self):
        return PostQueryset(self.model, using =self._db)

    def search(self, query= None):
        return self.get_queryset().search(query=query)
