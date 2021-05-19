from django.urls import path, include
from groups import views


urlpatterns = [
    path('Group/create', views.GroupCreateView.as_view()),
    path('Group/<int:pk>/detail', views.GroupRUdView.as_view()),
    path('Group/<int:pk>/update', views.GroupUpdateView.as_view()),
    path('Group/<int:id>/followers', views.GroupFollowerView.as_view()),
    path('Group/<int:id>/requests', views.GroupRequestView.as_view()),
    path('Group/<int:id>/admins', views.GroupAdminUserView.as_view()),
    path('Group/<int:id>/users', views.GroupUserView.as_view()),
    path('Group/', views.GroupListView.as_view()),
    path('Group/action', views.GroupActionView.as_view()),
    path('Group/admins_action', views.GroupAdminActionView.as_view()),
    path('Group/owner_action', views.GroupOwnerActionView.as_view()),
    path('Group/<int:pk>/followerslist', views.FollowersListView.as_view()),
    path('Group/<int:pk>/userlist', views.UsersListView.as_view()),
    path('Group/<int:pk>/adminlist', views.AdminListView.as_view()),
    

    # Blog Urls
    path('Group/MyBlog/create', views.BlogCreatePostView.as_view()),
    path('Group/MyBlog/<int:pk>/detail', views.BlogPostRUDView.as_view()),
    path('Group/MyBlog/<int:pk>/report', views.BlogReportsPostsView.as_view()),
    path('Group/MyBlog/<int:pk>/reportuser', views.BlogReportUseraView.as_view()),
    path('Group/MyBlog/<int:id>/Likes', views.BlogLikeListView.as_view()),
    path('Group/MyBlog/<int:pk>/', views.BlogPostListView.as_view()),
    path('Group/MyBlog/action', views.BlogActionView.as_view()),
    path('Group/MyBlog/report_action', views.BlogReportActionView.as_view()),

    #Comment Urls
    path('Group/comment/create', views.CommentCreatePostView.as_view()),
    path('Group/comment/<int:pk>/detail', views.CommentPostRUDView.as_view()),
    path('Group/comment/<int:id>/Likes', views.CommentLikeListView.as_view()),
    path('Group/comment/', views.CommentPostListView.as_view()),
    path('Group/comment/action', views.CommentActionView.as_view()),

    #SubComment Urls
    path('Group/subcomments/create', views.SubCommentCreatePostView.as_view()),
    path('Group/subcomments/<int:pk>/detail', views.SubCommentPostRUDView.as_view()),
    path('Group/subcomments/<int:id>/Likes', views.SubCommentLikeListView.as_view()),
    path('Group/subcomments/', views.SubCommentPostListView.as_view()),
    path('Group/subcomments/action', views.SubCommentActionView.as_view()),

]
