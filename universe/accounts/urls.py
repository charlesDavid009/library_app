from accounts import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('Account/register/', views.RegisterUserPostView.as_view()),
    path('Account/login/', views.LoginView.as_view()),
    path("Account/refresh/token/", TokenRefreshView.as_view(), name="token_refresh"),
    path('Account/email-verify/', views.VerifyEmail.as_view(), name="email-verify"),
    path('Account/request/reset-password', views.RequestPasswordResetEmail.as_view(), name = "reset-password"),
    path('Account/password-reset-confirm/<uidb64>/<token>/', views.PasswordTokenCheckAPI.as_view(), name = "password-reset-confirm"),
    path('Account/password-reset-complete/', views.SetNewPasswordAPIView.as_view(), name = "password-reset-complete")

]

