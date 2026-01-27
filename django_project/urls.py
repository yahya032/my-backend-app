from django.urls import path, include
from python_project.admin import admin_site
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/', include('python_project.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
