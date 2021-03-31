from django.shortcuts import render
from itertools import chain
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import SearchSerializer
from pages.models import Page, Blogs
from blog.models import Blog
from groups.models import Group, MyBlog
from profiles.models import Profile

class SearchView(generics.ListAPIView):
    serializer_class         = SearchSerializer
    permission_classes       = [IsAuthenticated]

    #def get_context_data(self, *args, **kwargs):
        #context = super().get_context_data(*args, **kwargs)
        #context['count'] = self.count or 0
        #context['query'] = self.request.GET.get('q')
        #return context

    def get_queryset(self):
        serializer = SearchSerializer(data = self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            query = data.get('query')

        if query is not None:
            blog_results        = Blog.objects.search(query)
            page_results      = Page.objects.search(query)
            pages_blog_results = Blogs.objects.search(query)
            groups_results      = Group.objects.search(query)
            groups_blog_results = MyBlog.objects.search(query)
            profile_results     = Profile.objects.search(query)

            # combine querysets
            queryset_chain = chain(
                    blog_results,
                    page_results,
                    pages_blog_results,
                    groups_results,
                    groups_blog_results,
                    profile_results
                    )
            qs = sorted(queryset_chain,
                        key=lambda instance: instance.pk,
                        reverse=True)
            self.count = len(qs) # since qs is actually a list
            return qs
        return Blog.objects.none() # just an empty queryset as default


class HomeView(generics.ListAPIView):
    serializer_class         = SearchSerializer
    permission_classes       = [IsAuthenticated]

    def get_queryset(self):
        blog_results        = Blog.objects.all()
        page_results      = Page.objects.all()
        pages_blog_results = Blogs.objects.all()
        groups_results      = Group.objects.all()
        groups_blog_results = MyBlog.objects.all()
        profile_results     = Profile.objects.all()

        # combine querysets
        queryset_chain = chain(
                blog_results,
                page_results,
                pages_blog_results,
                groups_results,
                groups_blog_results,
                profile_results
                )
        qs = sorted(queryset_chain,
                    key=lambda instance: instance.pk,
                    reverse=True)
        self.count = len(qs) # since qs is actually a list
        return qs

