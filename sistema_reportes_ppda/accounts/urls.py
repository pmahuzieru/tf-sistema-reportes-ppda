from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accounts.views import RegisterUserAPIView

urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name='register_users'),
]