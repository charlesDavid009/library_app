from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from .serializers import(
    CreateBlogSerializer,
    BlogSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    CreateSubCommentSerializer,
    SubCommentSerializer,
    ActionBlogSerializer,
    BlogLikesSerializer,
    CommentLikesSerializer,
    SubCommentLikesSerializer
)
from .models import (
    Blog,
    Comment,
    SubComment,
    BlogLikes,
    CommentLikes,
    SubCommentLikes
)
from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsOwner
from django.conf import settings
from django.db.models import Q


ACTIONS = settings.ACTIONS


# Create your views here.

# All About Blog Posts
class BlogPostRUDView(generics.RetrieveDestroyAPIView):
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Blog.objects.all()


class BlogCreatePostView(generics.CreateAPIView):
    lookup                  = 'pk'
    serializer_class        = CreateBlogSerializer
    permission_classes      = [IsAuthenticated]

    def get_queryset(self):
        return Blog.objects.all()

    def perform_create(self, serializer):
        users = self.request.user
        serializer.save(user= users)

class BlogDraftRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Blog.drafts.all()


class BlogDraftListView(generics.ListAPIView):
    """
    Get All Drafts
    """
    lookup                   = 'pk'
    serializer_class         = BlogSerializer
    permission_classes       = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        qs = Blog.drafts.all()
        user  = self.request.user
        obj = qs.filter(user= user)
        return obj


class BlogPostListView(generics.ListAPIView):
    """
    Get All Blogs And Search for Blog Titles Or Contents
    """
    lookup                   = 'pk'
    serializer_class         = BlogSerializer
    permission_classes       = [IsAuthenticated]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        qs = Blog.objects.all()
        query = self.request.GET.get("q")
        if query is not None:
            search = Blog.objects.search(query=query)
            return search
        return qs

class BlogUsersPostsView(generics.ListAPIView):
    """
    Displays Only Users Posts
    """
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated]

    def get_queryset(self):
        qs = Blog.objects.all()
        user  = self.request.user
        obj = qs.filter(user= user)
        return obj


class BlogFeedsView(generics.ListAPIView):
    """
    Displays Only Users Posts and users he follows
    """
    serializer_class         = BlogSerializer
    permission_classes       = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Blog.objects.feed(user)
        return qs


class BlogLikeListView(generics.ListAPIView):
    """
    Displays Only Users Posts
    """
    lookup                   = 'id'
    serializer_class         = BlogLikesSerializer
    permission_classes       = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = BlogLikes.objects.filter(blog=blog_id)
        return qs

class BlogActionView(generics.CreateAPIView):

    queryset = Blog.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs): #- Returns a serializer instance.
        serializer = ActionBlogSerializer(data = self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get('id')
            action = data.get('action')
            details = data.get('add')
            stat = data.get('status')
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
                    obj.reports.add(request.user)
                    serializer = BlogSerializer(obj)
                    return Response(serializer.data)
            elif action == "reblog":
                new_blog = Blog.objects.create(
                    user=request.user,
                    parent=obj,
                    content=details,
                    status= stat
                )
                serializer = BlogSerializer(new_blog)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)




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
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comment.objects.all()


class CommentCreatePostView(generics.CreateAPIView):
    """
    Create A Comment
    """
    lookup = 'pk'
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.all()

    def perform_create(self, serializer):
        users=self.request.user
        serializer.save(user=users)


class CommentPostListView(generics.ListAPIView):
    """
    Get All Comment Realated To A Blog
    """
    lookup = 'pk'
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        blog_id = self.kwargs.get('pk')
        qs = Comment.objects.filter(blog = blog_id)
        return qs

class CommentLikeListView(generics.ListAPIView):
    """
    Displays Only Comment Likes user
    """
    lookup = 'id'
    serializer_class = CommentLikesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = CommentLikes.objects.filter(blog=blog_id)
        return qs


class CommentActionView(generics.CreateAPIView):
    """
    Actions Like Or Unlike on Comment
    """
    queryset = Comment.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            comment_id = data.get('id')
            action = data.get('action')
            queryset = self.get_queryset()
            qs = queryset.filter(id=comment_id)
            if not qs.exists():
                return Response({}, status=staus.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(self.request.user)
                serializer = CommentSerializer(obj)
                #print(serializer.data)
                return Response(serializer.data)
            elif action == "unlike":
                    obj.like.remove(request.user)
                    serializer = CommentSerializer(obj)
                    return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


# ALL ABOUT SubCOMMENTS POSTS


class SubCommentPostRUDView(generics.RetrieveDestroyAPIView):
    """
    Get A SubComment Deatils With Its Id 
    """
    lookup = 'pk'
    serializer_class = SubCommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return SubComment.objects.all()


class SubCommentCreatePostView(generics.CreateAPIView):
    """
    Create A SubComment
    """
    #queryset = Comment.objects.all()
    lookup = 'pk'
    serializer_class = CreateSubCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubComment.objects.all()

    def perform_create(self, serializer):
        users=self.request.user
        serializer.save(user=users)
        """serializer = CreateSubCommentSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            comment_id = data.get('comment_id')
            text = data.get('text')
            queryset = Comment.objects.all()
            qs = queryset.filter(id=comment_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            obj_id =obj.blog
            new_comment = SubComment.objects.create(
                blog = obj_id,
                user = users,
                comment = str(qs),
                text = text
            )
            serializer = SubCommentSerializer(new_comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)"""


class SubCommentPostListView(generics.ListAPIView):
    """
    Get All SubComment Related To Comment Id   
    """
    lookup = 'pk'
    serializer_class = SubCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        blog_id = self.kwargs.get('pk')
        qs = SubComment.objects.filter(comment=blog_id)
        return qs


class SubCommentLikeListView(generics.ListAPIView):
    """
    Displays Only Users Likes
    """
    lookup = 'id'
    serializer_class = SubCommentLikesSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = SubCommentLikes.objects.filter(comment=blog_id)
        return qs


class SubCommentActionView(generics.CreateAPIView):
    """
    Actions Like Or Unlike On SubComment
    """
    queryset = SubComment.objects.all()
    serializer_class = ActionBlogSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionBlogSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            comment_id = data.get('id')
            action = data.get('action')
            queryset = self.get_queryset()
            qs = queryset.filter(id=comment_id)
            if not qs.exists():
                return Response({}, status=staus.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.like.add(self.request.user)
                serializer = SubCommentSerializer(obj)
                #print(serializer.data)
                return Response(serializer.data)
            elif action == "unlike":
                    obj.like.remove(request.user)
                    serializer = SubCommentSerializer(obj)
                    return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
