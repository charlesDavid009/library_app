from django.urls import path, include
from blog import views

urlpatterns = [
    path('Blog/create', views.BlogCreatePostView.as_view()),
    path('Blog/<int:pk>/detail', views.BlogPostRUDView.as_view()),
    path('Draft/<int:pk>/detail', views.BlogDraftRUDView.as_view()),
    path('Blog/user', views.BlogUsersPostsView.as_view()),
    path('Blog/feeds', views.BlogFeedsView.as_view()),
    path('Blog/<int:id>/likes', views.BlogLikeListView.as_view()),
    path('Blog/', views.BlogPostListView.as_view()),
    path('Draft/', views.BlogDraftListView.as_view()),
    path('Blog/action', views.BlogActionView.as_view()),

    #Comment Urls

    path('Comment/create', views.CommentCreatePostView.as_view()),
    path('Comment/<int:pk>/detail', views.CommentPostRUDView.as_view()),
    path('Comment/<int:id>/likes', views.CommentLikeListView.as_view()),
    path('Comment/<int:pk>/', views.CommentPostListView.as_view()),
    path('Comment/action', views.CommentActionView.as_view()),

    #SubComment Urls

    path('SubComment/create', views.SubCommentCreatePostView.as_view()),
    path('SubComment/<int:pk>/detail', views.SubCommentPostRUDView.as_view()),
    path('SubComment/<int:id>/likes', views.SubCommentLikeListView.as_view()),
    path('SubComment/<int:pk>/', views.SubCommentPostListView.as_view()),
    path('SubComment/action', views.SubCommentActionView.as_view()),

]
