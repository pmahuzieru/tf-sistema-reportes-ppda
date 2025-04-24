from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from sistema_reportes_ppda.settings.base import DEBUG
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mgmt/', include('management.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/reporting/', include('reporting.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]

if DEBUG:
    urlpatterns += [
        # drf-spectacular
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('spectacular/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='spectacular-swagger-ui'),
        path('spectacular/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='spectacular-redoc'),

    ]
