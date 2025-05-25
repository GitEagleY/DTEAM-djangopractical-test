"""
URL configuration for CVProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from main.views import CVDetailView, CVListView, recent_requests, settings_view, generate_pdf, send_cv_email

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from main.api_views import (
    CVAPIView, CVDetailedAPIView)

urlpatterns = [
    path(
        "cv/<int:pk>/",  # example: cv/1/
        CVDetailView.as_view(),
        name="template_detail"
    ),
    path('admin/', admin.site.urls),
    path("", CVListView.as_view(), name="template_list"),

    path('api/cvs/', CVAPIView.as_view(),
         name='api-cv-list'),
    path('api/cvs/<int:pk>/', CVDetailedAPIView.as_view(),
         name='api-cv-detail'),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='api-schema'), name='api-redoc'),
    
    path("logs/", recent_requests, name="recent_requests"),
    
    path("settings/", settings_view, name="settings"),
    
    path("cv/<int:pk>/pdf/", generate_pdf, name="cv-pdf"),
    
    path("cv/<int:pk>/send-email/", send_cv_email, name="cv-send-email"),
]