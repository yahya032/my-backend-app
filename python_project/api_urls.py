from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityViewSet,
    SpecialityViewSet,
    LevelViewSet,
    SemesterViewSet,
    MatiereViewSet,
    DocumentViewSet,
    list_firebase_users,
    create_firebase_user
)
from django.conf import settings
from django.conf.urls.static import static
from python_project.admin_site import admin_site

# Router DRF
router = DefaultRouter()
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'specialities', SpecialityViewSet, basename='speciality')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'documents', DocumentViewSet, basename='document')

# URL patterns
urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/', include(router.urls)),
    path('api/firebase-users/', list_firebase_users, name='firebase-users'),
    path('api/firebase-create-user/', create_firebase_user, name='firebase-create-user'),
]

# Servir les fichiers médias en DEV et PROD
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
