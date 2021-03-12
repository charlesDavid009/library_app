from django.shortcuts import render

from itertools import chain
from django.views.generic import ListView
from pages.models import Page, Blogs
from blog.models import Blog
from groups.models import Group, MyBlog
from profiles.models import Profile

class SearchView(ListView):
    #template_name = 'search/view.html'
    #paginate_by = 20
    #count = 0
    
    #def get_context_data(self, *args, **kwargs):
        #context = super().get_context_data(*args, **kwargs)
        #context['count'] = self.count or 0
        #context['query'] = self.request.GET.get('q')
        #return context

    def get_queryset(self):
        request = self.request
        query = request.GET.get('q', None)

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
        return Post.objects.none() # just an empty queryset as default
