from accounts import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('Account/register/', views.RegisterUserPostView.as_view()),
    path('Account/login/', views.LoginView.as_view()),
    path("Account/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("Account/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('Account/email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
]

