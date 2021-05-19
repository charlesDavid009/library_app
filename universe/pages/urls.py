from django.urls import path, include
from pages import views


urlpatterns = [
    #Page Urls
    path('Page/create', views.CreatePageView.as_view()),
    path('Page/<int:pk>/detail', views.PageRUDView.as_view()),
    path('Page/<int:id>/likes', views.LikeListView.as_view()),
    path('Page/<int:pk>/follows', views.FollowView.as_view()),
    path('Page/action', views.PageActionView.as_view()),
    path('Page/', views.PageListView.as_view()),

    #Blogs Urls
    path('Page/Blogs/create', views.BlogCreatePostView.as_view()),
    path('Page/Blogs/<int:pk>/detail', views.BlogPostRUDView.as_view()),
    path('Page/Blogs/<int:id>/likes', views.BlogLikeListView.as_view()),
    path('Page/Blogs/<int:pk>/', views.BlogPostListView.as_view()),
    path('Page/Blogs/action', views.BlogActionView.as_view()),

    #Comment Urls
    path('Page/Comments/create', views.CommentCreatePostView.as_view()),
    path('Page/Comments/<int:pk>/detail', views.CommentPostRUDView.as_view()),
    path('Page/Comments/<int:id>/likes', views.CommentLikeListView.as_view()),
    path('Page/Comments/<int:pk>/', views.CommentPostListView.as_view()),
    path('Page/Comments/action', views.CommentActionView.as_view()),
]
