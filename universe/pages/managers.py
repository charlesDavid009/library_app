from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from taggit.managers import TaggableManager

USER = get_user_model()


class PageQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug_icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class PageManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return PageQuerySet(self.model, using=self._db)

    def search(self, user, query=None):
        qs = self.get_queryset().search(query=query)
        return qs


class BlogsQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(slug_icontains=query))
            qs = qs.filter(or_lookup).distinct()
        return qs

class BlogsManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return BlogsQuerySet(self.model, using=self._db)

    def search(self, user, query= None):
        qs  = self.get_queryset().search(query=query)
        return qs
