from rest_framework.routers import DefaultRouter
from management.views import EnvironmentalPlanViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'environmental-plans', EnvironmentalPlanViewSet, basename='environmentalplan')

urlpatterns = [
    path('', include(router.urls))
]