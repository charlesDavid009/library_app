from django.urls import path, include
from profiles import views


urlpatterns = [
    #path('Profile/create', views.CraeteProfileView.as_view()),
    path('Profile/<int:pk>/detail', views.UpdateProfileView.as_view()),
    path('Profile/user', views.MyProfileView.as_view()),
    path('Profile/', views.GetUserView.as_view()),
    path('Profile/<int:id>/followers', views.UsersFollowersView.as_view()),
    path('Profile/<int:id>/following', views.UserFollowingView.as_view()),
    path('Profile/action', views.ProfileActionView.as_view()),
]
