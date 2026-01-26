from django.db import models
from django.contrib.auth.models import User
# ---------------- Alert ----------------
class Alert(models.Model):
    user_id = models.CharField(max_length=255)  # correspond au UID Firebase
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user_id})"
# ---------------- University ----------------
class University(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='universities/', blank=True, null=True)
    calendar = models.FileField(upload_to='calendars/', blank=True, null=True)  # PDF calendrier

    def __str__(self):
        return self.name

    # Méthode pour obtenir l'URL du calendrier
    def get_calendar_url(self):
        if self.calendar:
            return self.calendar.url
        return None

# ---------------- Speciality ----------------
class Speciality(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.CASCADE,
        related_name='specialities'
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "specialities"

    def __str__(self):
        return f"{self.name} - {self.university.name}"

# ---------------- Level ----------------
class Level(models.Model):
    name = models.CharField(max_length=10)  # Ex: L1, L2, L3, M1, M2

    def __str__(self):
        return self.name

# ---------------- Semester ----------------
class Semester(models.Model):
    name = models.CharField(max_length=10)  # Ex: S1, S2, ...
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='semesters'
    )

    def __str__(self):
        return f"{self.level.name} - {self.name}"

# ---------------- Matiere ----------------
class Matiere(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.CASCADE,
        related_name='matieres'
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.CASCADE,
        related_name='matieres'
    )

    def __str__(self):
        return f"{self.name} ({self.semester})"

# ---------------- Document ----------------
class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='documents'
    )

    def __str__(self):
        return self.title

    # Méthode pour obtenir l'URL du document
    def get_file_url(self):
        if self.file:
            return self.file.url
        return None
