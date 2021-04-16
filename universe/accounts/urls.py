from accounts import views
from django.urls import path

urlpatterns = [
    path('Account/register/', views.RegisterUserPostView.as_view()),
    path('Account/login/', views.LoginView.as_view()),
]
