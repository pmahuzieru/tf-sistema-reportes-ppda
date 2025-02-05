from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import CustomUserViewSet
from management.views import EnvironmentalPlanViewSet, MeasureReportViewSet, MeasureViewSet, ReportFileViewSet, BodyViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'environmental-plans', EnvironmentalPlanViewSet, basename='environmentalplan')
router.register(r'measures', MeasureViewSet, basename='measure')
router.register(r'reports', MeasureReportViewSet, basename='report')
router.register(r'files', ReportFileViewSet, basename='file')
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'bodies', BodyViewSet, basename='body')


urlpatterns = [
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
