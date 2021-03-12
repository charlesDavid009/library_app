from django.contrib import admin
from .models import (
    Blogs,
    BlogLiked,
    Comments,
    CommentLiked,
    Page,
    Following,
    Liking
)

# Register your models here.


class PageFollowAdmin(admin.TabularInline):
    model = Following

class PageLikesAdmin(admin.TabularInline):
    model = Liking


class PageAdmin(admin.ModelAdmin):
    inlines = [PageFollowAdmin, PageLikesAdmin]
    list_display = ['name', 'users', 'created']

    search_feild = ['name']

    class Meta:
        model = Page


class CommentLikesAdmin(admin.TabularInline):
    model = CommentLiked


class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentLikesAdmin]
    list_display = ['text', 'blog', 'user',  'user_info']

    search_feild = ['blog']

    class Meta:
        model = Comments


class BlogLikesAdmin(admin.TabularInline):
    model = BlogLiked


class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogLikesAdmin]
    list_display = ['title', 'created', 'user',  'owner']

    search_feild = ['title']

    class Meta:
        model = Blogs

admin.site.register(Blogs, BlogAdmin)
admin.site.register(Comments, CommentAdmin)
admin.site.register(Page, PageAdmin)
