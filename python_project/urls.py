# django_project/python_project/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UniversityViewSet, SpecialityViewSet, LevelViewSet,
    SemesterViewSet, MatiereViewSet, DocumentViewSet
)

router = DefaultRouter()
router.register(r'universities', UniversityViewSet)
router.register(r'specialities', SpecialityViewSet)
router.register(r'levels', LevelViewSet)
router.register(r'semesters', SemesterViewSet)
router.register(r'matieres', MatiereViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
