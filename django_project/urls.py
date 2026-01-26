# django_project/urls.py
from django.urls import path, include
from python_project.admin import admin_site  # ton admin custom
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin_site.urls),            # admin custom
    path('api/', include('python_project.urls')),  # API DRF
]

# ⚠️ Servir les fichiers media en dev (PDF, images, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
