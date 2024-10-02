from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("admin/", admin.site.urls),
    path(
        "update/", include("firmware_manager.urls")
    ),  # Rute pentru ESP32 și date seriale
    path("", include("light_app.urls")),
    path("summernote/", include("django_summernote.urls")),
]
