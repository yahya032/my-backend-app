# python_project/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# ⚠️ Correction de l'import : admin_site vient de admin_site.py
from python_project.admin_site import admin_site

from python_project.views import (
    UniversityViewSet,
    SpecialityViewSet,
    LevelViewSet,
    SemesterViewSet,
    MatiereViewSet,
    DocumentViewSet,
    list_firebase_users,
    create_firebase_user,
    user_alerts,
)

# 🔹 Router DRF pour les ViewSets
router = DefaultRouter()
router.register(r'universities', UniversityViewSet, basename='university')
# Décommenter si tu veux exposer les spécialités via l'API
# router.register(r'specialities', SpecialityViewSet, basename='speciality')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'documents', DocumentViewSet, basename='document')

# 🔹 URL patterns
urlpatterns = [
    path('admin/', admin_site.urls),              # Admin personnalisé
    path('api/', include(router.urls)),          # Toutes les routes des ViewSets
    path('api/firebase-users/', list_firebase_users, name='firebase-users'),
    path('api/firebase-create-user/', create_firebase_user, name='firebase-create-user'),
    path('api/alerts/', user_alerts, name='user-alerts'),
]

# 🔹 Servir les fichiers médias même en production
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
