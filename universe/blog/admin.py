from django.contrib import admin
from .models import (
    Blog,
    BlogLikes,
    Report,
    Comment,
    CommentLikes,
    SubComment,
    SubCommentLikes,
    ReportDetail
)

# Register your models here.


class ReportDetailAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user',  'created']

    search_feild = ['blog']

    class Meta:
        model = ReportDetail
class SubCommentLikesAdmin(admin.TabularInline):
    model = SubCommentLikes


class SubCommentAdmin(admin.ModelAdmin):
    inlines = [SubCommentLikesAdmin]
    list_display = ['comment', 'user',  'user_info']

    search_feild = ['comment']

    class Meta:
        model = SubComment


class CommentLikesAdmin(admin.TabularInline):
    model = CommentLikes


class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentLikesAdmin]
    list_display = [ 'blog', 'user',  'user_info']

    search_feild = ['blog']

    class Meta:
        model = Comment


class ReportsAdmin(admin.ModelAdmin):
    model = Report


class BlogLikesAdmin(admin.TabularInline):
    model = BlogLikes


class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogLikesAdmin]
    list_display = ['title', 'created', 'user']

    search_feild = ['title']

    class Meta:
        model = Blog


admin.site.register(Report, ReportsAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(SubComment, SubCommentAdmin)
