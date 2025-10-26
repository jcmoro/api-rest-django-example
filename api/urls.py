"""
Rutas globales del proyecto.
Incluye el admin y las rutas de la app `tasks`.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tasks.urls")),
]
