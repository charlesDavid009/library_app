from rest_framework import serializers
from .models import Blog, Comment, SubComment, BlogLikes, CommentLikes, SubCommentLikes, ReportDetail
from django.conf import settings
from accounts.serializer import UserInfoSerializer

ACTIONS = settings.ACTIONS


class CreateBlogSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created = serializers.DateTimeField(read_only=True)
    slug = serializers.CharField(read_only = True)
    class Meta:
        model = Blog
        fields = [ 'id', 'title', 'content', 'picture', 'slug', 'status', 'created']

    def create(self, validated_data):
        return Blog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.save()
        return instance



class BlogSerializer(serializers.ModelSerializer):
    reports = serializers.SerializerMethodField(read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)
    user = UserInfoSerializer(read_only =True)

    class Meta:
        ref_name = "blog 1"
        model = Blog
        fields = '__all__'


    def get_reports(self, obj):
        return obj.reports.count()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comments(self, obj):
        comment = obj.comments.count()
        return comment

    def get_content(self, obj):
        content = obj.content
        if obj.is_reblog:
            content = obj.parent.content
            return content


class BlogLikesSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only =True)
    class Meta:
        ref_name = "blog 2"
        model = BlogLikes
        fields = '__all__'

class BlogCreateReportSerialiizer(serializers.ModelSerializer):
    class Meta:
        ref_name = "blog 3"
        model = ReportDetail
        fields = ["blog", "context"]

    def create(self, validated_data):
        return ReportDetail.objects.create(**validated_data)

class BlogReportSerialiizer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only =True)
    class Meta:
        ref_name = "blog 3"
        model = ReportDetail
        fields = "__all__"
class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "blog 2"
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.blog_id = validated_data.get('blog_id', instance.blog_id)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    user = UserInfoSerializer(read_only =True)

    class Meta:
        ref_name = "blog 2"
        model = Comment
        fields = '__all__'

    def get_like(self, obj):
        return obj.like.count()

    def get_comment(self, obj):
        return obj.comment.count()


class CommentLikesSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only =True)
    class Meta:
        ref_name = "blog 2"
        model = CommentLikes
        fields = '__all__'


class CreateSubCommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    comment_id = serializers.IntegerField(required=True)
    text = serializers.CharField(required=True, max_length=9000)
    created = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return SubComment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.comment_id = validated_data.get('comment_id', instance.comment_id)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class SubCommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    user = UserInfoSerializer(read_only =True)

    class Meta:
        model = SubComment
        fields = '__all__'

    def get_like(self, obj):
        return obj.like.count()


class SubCommentLikesSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only =True)
    class Meta:
        model = SubCommentLikes
        fields = '__all__'


class ActionBlogSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    add = serializers.CharField(required=False, allow_blank=True)
    status = serializers.CharField(default= 'publish', required = False)

    def validate_action(self, value):
        value = value.lower().strip()
        if not value in ACTIONS:
            raise serializers.ValidationError(status=400)
        return value

class blogActionBlogSerializer(ActionBlogSerializer):
    class Meta:
        ref_name = 'blog 2'