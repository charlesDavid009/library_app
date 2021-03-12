from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.response import Response
from .serializers import (
    GroupSerializer,
    CreateGroupSerializer,
    CreateBlogSerializer,
    BlogSerializer,
    MessageSerializer,
    CreateMessageSerializer,
    ActionBlogSerializer,
    ActionReportSerializer,
    CommentSerializer,
    CreateCommentSerializer,
    RequestSerializer,
    FollowsSerializer,
    UsesSerializer,
    MyBlogLikesSerializer,
    MessageLikesSerializer,
    CommentLikesSerializer,
    AdminSerializer,
    ReportSerializer,
    ReportListSerializer
)
from .models import (
    Group,
    MyBlog,
    Message,
    MyComment,
    Request,
    Follows,
    Uses,
    CommentsLikes,
    MessageLikes,
    MyBlogLikes,
    Admins,
    Reports
)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .permissions import IsFollower, IsOwnerOrReadOnly, MyAdmin, IsOwners, IsUsers

User = get_user_model()

ACTIONS = settings.ACTIONS

# Create your views here.

class GroupCreateView(generics.CreateAPIView):
    """
    Create Group
    """
    serializer_class = CreateGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Group.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = CreateGroupSerializer(data= request.data)
        if serializer.is_valid():
            obj = serializer.save(owner = self.request.user)
            vs = obj.id
            qs = Group.objects.filter(id = vs)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            objs = qs.first()
            objs.follower.add(self.request.user)
            objs.users.add(self.request.user)
            objs.admin.add(self.request.user)
            serializers = objs.save()
            return Response(serializers, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

class GroupListView(generics.ListAPIView):
    """
    Display Group List
    """
    lookup                  = 'pk'
    serializer_class        = GroupSerializer
    permission_classes      = [IsAuthenticated]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        qs = Group.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)).distinct()
        return qs


class GroupRUdView(generics.RetrieveUpdateDestroyAPIView):
    """
    View And Delete Group Associated To Owner
    """
    lookup = 'pk'
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Group.objects.all()

class GroupUpdateView(generics.UpdateAPIView):
    """
    Update Group Associated To Owner
    """
    lookup = 'pk'
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        qs = Group.objects.filter(id =blog_id)
        return qs

class GroupFollowerView(generics.ListAPIView):
    """
    Display Follow User
    """
    lookup = 'id'
    serializer_class = FollowsSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Follows.objects.filter(groups=blog_id)
        return qs

class GroupRequestView(generics.ListAPIView):
    """
    Display Follow User
    """
    lookup = 'id'
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Request.objects.filter(group=blog_id)
        return qs

class GroupAdminUserView(generics.ListAPIView):
    """
    Display Group Admin
    """
    lookup = 'id'
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Admins.objects.filter(container=blog_id)
        return qs


class GroupUserView(generics.ListAPIView):
    """
    Display Group User
    """
    lookup = 'id'
    serializer_class = UsesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = Uses.objects.filter(members=blog_id)
        return qs


class GroupActionView(generics.CreateAPIView):
    """
    Actions On Groups
    """
    queryset = Group.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id_")
            action = data.get("action")
            qs = Group.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_401_UNAUTHORIZED)
            obj = qs.first()
            if action == "follow":
                obj.follower.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "unfollow":
                obj.follower.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "exit":
                obj.users.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "join":
                obj.request.add(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "invite":
                obj.like.remove(request.user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class GroupAdminActionView(generics.CreateAPIView):
    """
    Actions By Group Admin
    """
    queryset = Group.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated, MyAdmin]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            group_id = data.get("id_")
            action = data.get("action")
            qs = Request.objects.filter(id=group_id)
            if not qs.exists():
                return Response(status=status.HTTP_404_NOT_FOUND)
            vd = qs.first()
            user = vd.user
            obj = vd.group
            if action == "confirm":
                obj.users.add(user)
                vd = Group.objects.filter(follower=user)
                if not vd.exists():
                    obj.follower.add(user)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "reject":
                obj.request.remove(user)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "remove":
                obj.users.remove(user)
                vs = Group.objects.filter(follower=user)
                if vs.exists():
                    obj.follower.remove(user)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class GroupOwnerActionView(generics.CreateAPIView):
    """
    Actions By Group Admin
    """
    queryset = Group.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated, IsOwners]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            users_id = data.get("id_")
            action = data.get("action")
            qs = Uses.objects.filter(id=users_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            ms = qs.first()
            md = ms.user
            obj = ms.members
            if action == "add":
                obj.admin.add(md)
                vs = Group.objects.filter(follower=ms)
                if not vs.exists():
                    obj.follower.add(ms)
                    serializer = GroupSerializer(obj)
                    return Response(serializer.data)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            elif action == "remove":
                obj.admin.remove(md)
                serializer = GroupSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

class FollowersListView(generics.ListAPIView):
    """
    Displays All Users that Follows This Group
    """
    lookup                      ='pk'
    serializer_class            = FollowsSerializer
    permission_classes          = [IsFollower, IsUsers, IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        qs = Follows.objects.filter(groups= group_id)
        return qs
class UsersListView(generics.ListAPIView):
    """
    Displays All Users that Uses This Group
    """
    lookup = 'pk'
    serializer_class = UsesSerializer
    permission_classes = [IsFollower, IsUsers, IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        qs = Uses.objects.filter(members=group_id)
        return qs
class AdminListView(generics.ListAPIView):
    """
    Displays All Users that Admin This Group
    """
    lookup                      ='pk'
    serializer_class            = AdminSerializer
    permission_classes          = [IsFollower, IsUsers, IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs.get('pk')
        qs = Admins.objects.filter(container= group_id)
        return qs

# BLOG BRGINS AND END HERE

class BlogPostRUDView(generics.RetrieveDestroyAPIView):
    """
    Getting A Blog Post With its Id
    """
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated, IsOwnerOrReadOnly, IsFollower]

    def get_queryset(self):
        return MyBlog.objects.all()


class BlogCreatePostView(generics.CreateAPIView):
    """
    Creating a Blog
    """
    lookup                  = 'pk'
    serializer_class        = CreateBlogSerializer
    permission_classes      = [IsAuthenticated, IsUsers]

    def get_queryset(self):
        return MyBlog.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


class BlogPostListView(generics.ListAPIView):
    """
    Get All Blogs And Search for Blog Titles Or Contents
    """
    lookup                   = 'pk'
    serializer_class         = BlogSerializer
    permission_classes       = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        group_id = self.kwargs.get('pk')
        qs = MyBlog.objects.filter(reference = group_id)
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains = query)|
                Q(content__icontains = query)).distinct()
        return qs

class BlogReportsPostsView(generics.ListAPIView):
    """
    Displays Reports
    """ 
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated, MyAdmin]

    def get_queryset(self):
        _ids= self.kwargs.get('pk')
        qs = Reports.objects.filter(group = _ids)
        return qs

class BlogReportUseraView(generics.ListAPIView):
    """
    Displays Only Report User Lists
    """
    lookup                  = 'pk'
    serializer_class        = ReportListSerializer
    permission_classes      = [IsAuthenticated, MyAdmin]

    def get_queryset(self):
        _ids = self.kwargs.get('pk')
        qs = Reports.objects.filter(blog =_ids)
        return qs

class BlogLikeListView(generics.ListAPIView):
    """
    Displays Only Likes Lists
    """
    lookup                   = 'id'
    serializer_class         = MyBlogLikesSerializer
    permission_classes       = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = MyBlogLikes.objects.filter(blog=blog_id)
        return qs

class BlogActionView(generics.CreateAPIView):
    """
    API FOR ACTIONS LIKE, UNLIKE , REBLOG, REPORT ON BLOGS
    """
    queryset = MyBlog.objects.all()
    serializer_class = ActionReportSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs): #- Returns a serializer instance.
        serializer = ActionReportSerializer(data = self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get('id_')
            action = data.get('action')
            group = data.get('group_id')
            vs = Group.objects.filter(id = group)
            if not vs.exists():
                return Response({}, status = status.HTTP_404_NOT_FOUND)
            vd = vs.first()
            queryset = self.get_queryset()
            qs = queryset.filter(id = blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "report":
                obj.likes.add(self.request.user)
                serializer = BlogSerializer(obj)
                #print(serializer.data)
                return Response(serializer.data)

class BlogActionView(generics.CreateAPIView):
    """
    API FOR ACTIONS LIKE, UNLIKE , REBLOG, REPORT ON BLOGS
    """
    queryset = MyBlog.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs): #- Returns a serializer instance.
        serializer = ActionBlogSerializer(data = self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get('id_')
            action = data.get('action')
            til = data.get('title')
            add = data.get('add')
            group = data.get('group_id')
            vs = Group.objects.filter(id = group)
            if not vs.exists():
                return Response({}, status = status.HTTP_404_NOT_FOUND)
            vd = vs.first()
            queryset = self.get_queryset()
            qs = queryset.filter(id = blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.likes.add(self.request.user)
                serializer = BlogSerializer(obj)
                #print(serializer.data)
                return Response(serializer.data)
            elif action == "unlike":
                    obj.likes.remove(request.user)
                    serializer = BlogSerializer(obj)
                    return Response(serializer.data)
            elif action == "report":
                obj.report.add(request.user)
                vs = obj.reference_id
                qs = Reports.objects.filter(id=obj.id)
                qs = qs.first()
                qs = qs.save(group= vs)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)
            elif action == "reblog":
                vs = obj.reference_id
                new_blog = MyBlog.objects.create(
                    owner=request.user,
                    parent=obj,
                    reference_id=vs,
                    title=til,
                    content=add
                )
                serializer = BlogSerializer(new_blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

class BlogReportActionView(generics.CreateAPIView):
    """
    API FOR ACTIONS Pass,Remove ON BLOGS
    """
    queryset = MyBlog.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs): #- Returns a serializer instance.
        serializer = ActionBlogSerializer(data = self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id_")
            action = data.get("action")
            qs = MyBlog.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "pass":
                obj.report.remove(obj)
                serializer = RequestSerializer(obj)
                return Response(serializer.data)
            elif action == "remove":
                obj.delete(obj)
                serializer = BlogSerializer(obj)
                return Response(serializer.data)

#class UserList(generics.ListCreateAPIView):
    #queryset = User.objects.all()
    #serializer_class = UserSerializer
    #permission_classes = [IsAdminUser]

    #def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        #queryset = self.get_queryset()
        #serializer = UserSerializer(queryset, many=True)
        #return Response(serializer.data)


#get_serializer_context(self) - Returns a dictionary containing any extra context that should be supplied to the serializer. Defaults to including 'request', 'view' and 'format' keys.
#get_serializer(self, instance=None, data=None, many=False, partial=False) - Returns a serializer instance.


#class MultipleFieldLookupMixin:
    """
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """

    #def get_object(self):
        #queryset = self.get_queryset()             # Get the base queryset
        #queryset = self.filter_queryset(queryset)  # Apply any filter backends
        #filter = {}
        ##    if self.kwargs[field]:  # Ignore empty fields.
        #        filter[field] = self.kwargs[field]
        #obj = get_object_or_404(queryset, **filter)  # Lookup the object
        #self.check_object_permissions(self.request, obj)
        #return obj

# ALL ABOUT COMMENTS POSTS


class CommentPostRUDView(generics.RetrieveDestroyAPIView):
    """
    Get A Comment Details According To The Id
    """
    lookup = 'pk'
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsFollower, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Message.objects.all()


class CommentCreatePostView(generics.CreateAPIView):
    """
    Create A Comment
    """
    lookup = 'pk'
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated, IsUsers]

    def get_queryset(self):
        return Message.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner =self.request.user)


class CommentPostListView(generics.ListAPIView):
    """
    Get All Comment Realated To A Blog
    """
    lookup = 'pk'
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        blog_id = self.kwargs.get('pk')
        qs = Message.objects.filter(reference=blog_id)
        return qs

class CommentLikeListView(generics.ListAPIView):
    """
    Displays Only Comment Likes user
    """
    lookup           = 'id'
    serializer_class = MessageLikesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = MessageLikes.objects.filter(blog=blog_id)
        return qs


class CommentActionView(generics.CreateAPIView):
    """
    Actions Like Or Unlike on Comment
    """
    queryset = Message.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated, IsUsers]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            qs = Message.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(request.user)
                serializer = MessageSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.like.remove(request.user)
                serializer = MessageSerializer(obj)
                return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


# ALL ABOUT SubCOMMENTS POSTS


class SubCommentPostRUDView(generics.RetrieveDestroyAPIView):
    """
    Get A SubComment Deatils With Its Id 
    """
    lookup = 'pk'
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsFollower, IsOwnerOrReadOnly]

    def get_queryset(self):
        return MyComment.objects.all()


class SubCommentCreatePostView(generics.CreateAPIView):
    """
    Create A SubComment
    """
    lookup = 'pk'
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated, IsUsers]

    def get_queryset(self):
        return MyComment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owners =self.request.user)


class SubCommentPostListView(generics.ListAPIView):
    """
    Get All SubComment Related To Comment Id   
    """
    lookup = 'pk'
    serializer_class   = CommentSerializer
    permission_classes = [IsAuthenticated, IsFollower]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        blog_id = self.kwargs.get('pk')
        qs = MyComment.objects.filter(reference=blog_id)
        return qs


class SubCommentLikeListView(generics.ListAPIView):
    """
    Displays Only Users Likes
    """
    lookup = 'id'
    serializer_class = CommentLikesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsFollower]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = CommentsLikes.objects.filter(post=blog_id)
        return qs


class SubCommentActionView(generics.CreateAPIView):
    """
    Actions Like Or Unlike On SubComment
    """
    queryset = MyComment.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get("id")
            action = data.get("action")
            qs = MyComment.objects.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(request.user)
                serializer = CommentSerializer(obj)
                return Response(serializer.data)
            elif action == "unlike":
                obj.like.remove(request.user)
                serializer = CommentSerializer(obj)
                return Response(serializer.data)
