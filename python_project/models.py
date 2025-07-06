from django.db import models

class University(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='universities/')

    def __str__(self):
        return self.name

class Speciality(models.Model):
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='specialities')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.university.name}"

class Level(models.Model):
    name = models.CharField(max_length=10)  # Ex: L1, L2, L3, M1, M2

    def __str__(self):
        return self.name

class Semester(models.Model):
    name = models.CharField(max_length=10)  # Ex: S1, S2, ...
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='semesters')

    def __str__(self):
        return f"{self.level.name} - {self.name}"

class Matiere(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='matieres')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name='matieres')

    def __str__(self):
        return f"{self.name} ({self.semester})"

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, null=True, related_name='documents')

    def __str__(self):
        return self.title