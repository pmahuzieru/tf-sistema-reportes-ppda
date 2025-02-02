from rest_framework.routers import DefaultRouter
from management.views import EnvironmentalPlanViewSet, MeasureViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'environmental-plans', EnvironmentalPlanViewSet, basename='environmentalplan')
router.register(r'measure', MeasureViewSet, basename='measure')

urlpatterns = [
    path('', include(router.urls))
]