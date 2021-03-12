from .views import RegisterUserPostView, LoginUserPostView
from django.urls import path

urlpatterns = [
    path('Account/register/', RegisterUserPostView.as_view()),
    path('Account/login/', LoginUserPostView.as_view()),
]
