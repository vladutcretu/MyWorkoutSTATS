"""
URL configuration for MyWorkoutSTATS_app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# API documentation library
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# API JWT Auth
from rest_framework_simplejwt.views import TokenRefreshView


# 3rd party library
from debug_toolbar.toolbar import debug_toolbar_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("fitness.urls")),
    path("api/", include("core.api.urls")),
    path("api/", include("fitness.api.urls")),
    # API documentation urls
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # Allauth urls
    path("accounts/", include("allauth.urls")),
    # JWT auth urls
    path(
        "api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
] + debug_toolbar_urls()

# Needed for use media content (profile pics)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
