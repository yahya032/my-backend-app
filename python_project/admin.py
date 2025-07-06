#django_project/python_project/admin.py
from django.contrib import admin
from .models import University, Speciality, Level, Semester, Matiere, Document
admin.site.register(University)
admin.site.register(Speciality)
admin.site.register(Level)
admin.site.register(Semester)
admin.site.register(Matiere)
admin.site.register(Document)
