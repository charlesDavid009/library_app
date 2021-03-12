from django.contrib import admin
from .models import (
    Group,
    Uses,
    Follows,
    MyBlog,
    MyBlogLikes,
    MyComment,
    CommentsLikes,
    Message,
    MessageLikes,
    Admins,
    Reports
)

# Register your models here.


class MessageLikesAdmin(admin.TabularInline):
    model = MessageLikes


class MessageAdmin(admin.ModelAdmin):
    inlines = [MessageLikesAdmin]
    list_display = ['reference', 'owner']

    search_feild = ['reference']

    class Meta:
        model = Message


class CommentsLikesAdmin(admin.TabularInline):
    model = CommentsLikes

class CommentAdmin(admin.ModelAdmin):
    inlines = [CommentsLikesAdmin]
    list_display = ['reference', 'owners']

    search_feild = ['reference']

    class Meta:
        model = MyComment


class ReportsAdmin(admin.ModelAdmin):
    list_display = ['group', 'blog', 'users', 'created_at']
    search_field = ['group', 'blog']
    class Meta:
        model = Reports


class BlogLikesAdmin(admin.TabularInline):
    model = MyBlogLikes


class BlogAdmin(admin.ModelAdmin):
    inlines = [BlogLikesAdmin]
    list_display = ['reference', 'title', 'created_at', 'owner']

    search_feild = ['reference']

    class Meta:
        model = MyBlog


class FollowsAdmin(admin.TabularInline):
    model = Follows


class UsesAdmin(admin.TabularInline):
    model = Uses


class AdminsAdmin(admin.TabularInline):
    model = Admins


class GroupAdmin(admin.ModelAdmin):
    inlines = [FollowsAdmin, UsesAdmin, AdminsAdmin]
    list_display = ['group_name', 'created_at', 'owner']

    search_feild = ['group_name']

    class Meta:
        model = Group


admin.site.register(Group, GroupAdmin)
admin.site.register(MyBlog, BlogAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MyComment, CommentAdmin)
admin.site.register(Reports, ReportsAdmin)
