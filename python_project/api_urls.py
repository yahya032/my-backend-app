from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityViewSet,
    SpecialityViewSet,
    LevelViewSet,
    SemesterViewSet,
    MatiereViewSet,
    DocumentViewSet,
    list_firebase_users,      # 🔹 endpoint Firebase
    create_firebase_user      # 🔹 endpoint création Firebase
)

# 🔹 Création du router DRF pour les viewsets
router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'specialities', SpecialityViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'matieres', MatiereViewSet)
router.register(r'documents', DocumentViewSet)

# 🔹 URL patterns
urlpatterns = [
    path('', include(router.urls)),                           # Inclut toutes les routes des viewsets
    path('firebase-users/', list_firebase_users, name='firebase-users'),        # Lister les utilisateurs Firebase
    path('firebase-create-user/', create_firebase_user, name='firebase-create-user'),  # Créer un utilisateur Firebase
]
