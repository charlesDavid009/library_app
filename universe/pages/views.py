from django.shortcuts import render
from .models import(
    Blogs,
    Page,
    Liking,
    Following,
    BlogLiked,
    Comments,
    CommentLiked
)
from .serializers import(
    PageSerializer,
    CreatePageSerializer,
    FollowingSerializer,
    LikingSerializer,
    CreatePageBlogsSerializer,
    BlogSerializer,
    BlogLikedSerializer,
    CreateCommentSerializer,
    CommentSerializer,
    CommentLikesSerializer,
    ActionSerializer
)
from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly, IsOwner
from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

Action = settings.ACTIONS

# Create your views here.

class CreatePageView(generics.CreateAPIView):
    serializer_class = CreatePageSerializer
    permissions_classes = [IsAuthenticated]

    def get_queryset(self):
        return Page.objects.all()

    def perform_create(self, serializer):
        serializer.save(users = self.request.user)

class PageListView(generics.ListAPIView):
    serializer_class        = PageSerializer
    permisssions_classes    = [IsAuthenticated]

    def get_queryset(self):
        return Page.objects.all()

class PageRUDView(generics.RetrieveUpdateDestroyAPIView):
    lookup                      = 'pk'
    serializer_class            = PageSerializer
    permisssions_classes        = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Page.objects.all()

class FollowView(generics.ListAPIView):
    lookup                      ='pk'
    serializer_class            = FollowingSerializer
    permissions_classes         = [IsAuthenticated]

    def get_queryset(self):
        page_id = self.kwargs.get('pk')
        qs = Following.objects.filter(references = page_id)
        obj = qs.first()
        return obj

class LikeListView(generics.ListAPIView):
    lookup                      ='pk'
    serializer_class            = LikingSerializer
    permissions_classes         = [IsAuthenticated]

    def objects(self, request, *args, **kwargs):
        page_id = self.kwargs.get('pk')
        qs = Liking.objects.filter(referenced = page_id)


class PageActionView(generics.CreateAPIView):

    queryset = Page.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get('id')
            action = data.get('action')
            queryset = self.get_queryset()
            qs = queryset.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=status.HTTP_404_NOT_FOUND)
            obj = qs.first()
            if action == "like":
                obj.likes.add(self.request.user)
                serializer = PageSerializer(obj)
                #print(serializer.data)
                return Response(serializer.data)
            elif action == "unlike":
                    obj.likes.remove(request.user)
                    serializer = PageSerializer(obj)
                    return Response(serializer.data)
            elif action == "follow":
                    obj.following.add(request.user)
                    serializer = PageSerializer(obj)
                    return Response(serializer.data)
            elif action == "unfollow":
                    obj.following.remove(request.user)
                    serializer = PageSerializer(obj)
                    return Response(serializer.data)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class BlogPostRUDView(generics.RetrieveDestroyAPIView):
    lookup                  = 'pk'
    serializer_class        = BlogSerializer
    permission_classes      = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Blogs.objects.all()


class BlogCreatePostView(generics.CreateAPIView):
    lookup = 'pk'
    serializer_class = CreatePageBlogsSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Blogs.objects.all()

    def perform_create(self, serializer):
        serializer.save(user =self.request.user)


class BlogPostListView(generics.ListAPIView):
    """
    Get All Blogs And Search for Blog Titles Or Contents
    """
    lookup = 'pk'
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        To use search features, always put this before the url
        in the browser--> ?q=(the word you want to search for)
        """
        id_ = self.kwargs.get('pk')
        qs = Blogs.objects.filter(reference = id_)
        query = self.request.GET.get("q")
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)).distinct()
        return qs

class BlogLikeListView(generics.ListAPIView):
    """
    Displays Only Users Posts
    """
    lookup              = 'id'
    serializer_class    = BlogLikedSerializer
    permission_classes  = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        blog_id = self.kwargs.get('id')
        qs = BlogLiked.objects.filter(blogs =blog_id)
        return qs


class BlogActionView(generics.CreateAPIView):

    queryset = Blogs.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            blog_id = data.get('id')
            action = data.get('action')
            queryset = self.get_queryset()
            qs = queryset.filter(id=blog_id)
            if not qs.exists():
                return Response({}, status=staus.HTTP_404_NOT_FOUND)
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
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

# ALL ABOUT COMMENTS POSTS


class CommentPostRUDView(generics.RetrieveDestroyAPIView):
    """
    Get A Comment Details According To The Id
    """
    lookup = 'pk'
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return Comments.objects.all()


class CommentCreatePostView(generics.CreateAPIView):
    """
    Create A Comment
    """
    lookup = 'pk'
    serializer_class = CreateCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comments.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
        qs = Comments.objects.filter(blog=blog_id)
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
        qs = CommentLiked.objects.filter(blog=blog_id)
        return qs


class CommentActionView(generics.CreateAPIView):
    """
    Actions Like Or Unlike on Comment
    """
    queryset = Comments.objects.all()
    serializer_class = ActionSerializer
    permission_classes = [IsAuthenticated]

    # - Returns a serializer instance.
    def create(self, request, *args, **kwargs):
        serializer = ActionSerializer(data=self.request.data)
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
