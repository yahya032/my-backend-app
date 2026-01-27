from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('python_project.api_urls')),  # inclut toutes les URLs de l'app
]
