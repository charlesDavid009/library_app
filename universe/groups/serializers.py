from rest_framework import serializers
from .models import(
    Group,
    MyBlog,
    Message,
    MyComment,
    Request,
    Follows,
    Uses,
    MyBlogLikes,
    CommentsLikes,
    MessageLikes,
    Admins,
    Reports
)
from django.conf import settings

ACTIONS = settings.ACTIONS


class GroupSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField(read_only=True)
    follower = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        exclude = [ 'request','admin']

    def get_follower(self, obj):
        return obj.follower.count()

    def get_users(self, obj):
        return obj.users.count()

class CreateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['group_name', 'description', 'picture']

    def create(self, validated_data):
        return Group.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.group_name = validated_data.get(
            'group_name', instance.group_name)
        instance.picture = validated_data.get('picture', instance.picture)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.save()
        return instance


class CreateBlogSerializer(serializers.Serializer):
    class Meta:
        model = MyBlog
        fields = ['reference_id', 'title', 'content', 'picture']

    def create(self, validated_data):
        return MyBlog.objects.create(**validated_data)

class BlogSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    comment = serializers.SerializerMethodField(read_only=True)
    parent = CreateBlogSerializer(read_only=True)

    class Meta:
        model = MyBlog
        exclude = ['report']

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comment(self, obj):
        return obj.comment.count()

    def get_content(self, obj):
        content = obj
        if obj.is_reblog:
            content = obj.parent.content
            return content

    def get_title(self, obj):
        title = obj
        if obj.is_reblog:
            title = obj.parent.title
            return title


class MessageSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)
    comments = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Message
        fields = ["reference", "id", "comments", "like", "created_at"]

    def get_like(self, obj):
        return obj.like.count()

    def get_comments(self, obj):
        return obj.comments.count()


class CreateMessageSerializer(serializers.Serializer):
    reference = serializers.IntegerField()
    message = serializers.CharField()

    def create(self, validated_data):
        return Message.objects.create(**validated_data)


class ActionBlogSerializer(serializers.Serializer):
    id_ = serializers.IntegerField()
    action = serializers.CharField()
    title = serializers.CharField()
    add = serializers.CharField(required=False)
    group_id = serializers.IntegerField(required = False)

    def validate_action(self, value):
        value = value.lower().strip()
        if value in ACTIONS:
            return value
        return serializers.ValidationError(status=400)

class ActionReportSerializer(serializers.Serializer):
    id_ = serializers.IntegerField()
    action = serializers.CharField()
    group_id = serializers.IntegerField(required = False)

    def validate_action(self, value):
        value = value.lower().strip()
        if value in ACTIONS:
            return value
        return serializers.ValidationError(status=400)

class CommentSerializer(serializers.ModelSerializer):
    like = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = MyComment
        fields = ["reference", "id", "comment", "likes", "created_at"]

    def get_like(self, obj):
        return obj.like.count()


class CreateCommentSerializer(serializers.Serializer):
    reference = serializers.IntegerField()
    comment = serializers.CharField()

    def create(self, validated_data):
        return MyComment.objects.create(**validated_data)


class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = '__all__'


class UsesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uses
        fields = '__all__'


class FollowsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follows
        fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admins
        fields = '__all__'


class MyBlogLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyBlogLikes
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyBlog
        fields = '__all__'

    def get_report(self, obj):
        return obj.report.count()

    def get_likes(self, obj):
        return obj.likes.count()

    def get_comment(self, obj):
        return obj.comment.count()

class CreateReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = ["reasons"]

class ReportListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reports
        fields = '__all__'


class MessageLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageLikes
        fields = '__all__'


class CommentLikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = CommentsLikes
        fields = '__all__'
