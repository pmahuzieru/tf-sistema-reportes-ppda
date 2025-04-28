from django.urls import include, path
from rest_framework.routers import DefaultRouter
from accounts.views import RegisterUserModelViewSet


router = DefaultRouter()
router.register(r'register', RegisterUserModelViewSet, basename='register_users')

urlpatterns = [
    path('', include(router.urls)),
]
