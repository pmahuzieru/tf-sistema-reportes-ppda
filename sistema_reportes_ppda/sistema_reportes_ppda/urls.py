from django.contrib import admin
from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from sistema_reportes_ppda.settings import DEBUG
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/mgmt/', include('management.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/reporting/', include('reporting.urls')),
#    path('api/token/', obtain_auth_token, name='api_token')
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify')
]

if DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Sistema de Reportes PPDA (Grupo 2)",
            default_version='v1',
            description="Work in progress...",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@myapi.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    ]
