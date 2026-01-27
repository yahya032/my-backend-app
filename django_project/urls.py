from django.contrib import admin
from django.urls import path, include
from python_project.admin_site import get_admin_site
from django.conf import settings
from django.conf.urls.static import static

admin_site = get_admin_site()

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/', include('python_project.api_urls')),
]
# Servir les fichiers médias en dev ET prod
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
