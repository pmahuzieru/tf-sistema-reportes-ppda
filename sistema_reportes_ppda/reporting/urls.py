from rest_framework.routers import DefaultRouter
from django.urls import path, include
from reporting.views import ProgressReportViewSet

router = DefaultRouter()
router.register(r'progress-reports', ProgressReportViewSet, basename='progressreport')

urlpatterns = [
    path('', include(router.urls)),  # Ensure you're using 'urlpatterns' here, not 'url_patterns'
]