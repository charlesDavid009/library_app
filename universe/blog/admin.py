from django.contrib import admin
from .models import (
    Blog,
    BlogLikes,
    Report,
    Comment,
    CommentLikes,
    SubComment,
    SubCommentLikes
)

# Register your models here.


class SubCommentLikesAdmin(admin.TabularInline):
    model = SubCommentLikes


class SubCommentAdmin(admin.ModelAdmin):
    inlines = [SubCommentLikesAdmin]
    list_display = ['text', 'blog', 'user',  'user_info']

    search_feild = ['blog']

    class Meta:
        model = SubComment


class CommentLikesAdmin(admin.TabularInline):
    model = CommentLikes


class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentLikesAdmin]
    list_display = ['text', 'blog', 'user',  'user_info']

    search_feild = ['blog']

    class Meta:
        model = Comment


class ReportsAdmin(admin.ModelAdmin):
    model = Report


class BlogLikesAdmin(admin.TabularInline):
    model = BlogLikes


class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogLikesAdmin]
    list_display = ['title', 'created', 'user',  'owner']

    search_feild = ['title']

    class Meta:
        model = Blog


admin.site.register(Report, ReportsAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SubComment, SubCommentAdmin)
