# python_project/admin_site.py

from django.contrib.admin import AdminSite
from django.urls import path
from django.shortcuts import render
from .models import Alert, Document, University, Speciality, Level, Semester, Matiere


class CustomAdminSite(AdminSite):
    site_header = "Administration SupNum"
    site_title = "Dashboard Admin"
    index_title = "Résumé des données"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        context = dict(
            self.each_context(request),
            total_alerts=Alert.objects.count(),
            total_documents=Document.objects.count(),
            total_universities=University.objects.count(),
            total_specialities=Speciality.objects.count(),
            total_levels=Level.objects.count(),
            total_semesters=Semester.objects.count(),
            total_matieres=Matiere.objects.count(),
        )
        return render(request, "admin/custom_dashboard.html", context)
