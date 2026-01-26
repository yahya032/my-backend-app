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
    create_firebase_user,
    user_alerts,
)

# 🔹 Création du router DRF pour les ViewSets
router = DefaultRouter()
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'specialities', SpecialityViewSet, basename='speciality')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'documents', DocumentViewSet, basename='document')

# 🔹 URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Inclut toutes les routes des viewsets
    path('firebase-users/', list_firebase_users, name='firebase-users'),  # Liste des utilisateurs Firebase
    path('firebase-create-user/', create_firebase_user, name='firebase-create-user'),  # Création d'utilisateur Firebase
    path('alerts/', user_alerts, name='user-alerts'),  # Alertes utilisateur
]
