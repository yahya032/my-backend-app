from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from python_project.admin import admin_site
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

router = DefaultRouter()
router.register(r'universities', UniversityViewSet, basename='university')
router.register(r'specialities', SpecialityViewSet, basename='speciality')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'matieres', MatiereViewSet, basename='matiere')
router.register(r'documents', DocumentViewSet, basename='document')

urlpatterns = [
    path('admin/', admin_site.urls),
    path('api/', include(router.urls)),
    path('api/firebase-users/', list_firebase_users, name='firebase-users'),
    path('api/firebase-create-user/', create_firebase_user, name='firebase-create-user'),
    path('api/alerts/', user_alerts, name='user-alerts'),
]

# 🔹 Servir les fichiers médias sur Render
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
