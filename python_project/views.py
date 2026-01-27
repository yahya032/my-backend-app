from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.http import FileResponse
import os

# 🔹 Modèles
from .models import University, Speciality, Level, Semester, Matiere, Document, Alert

# 🔹 Serializers
from .serializers import (
    UniversitySerializer, SpecialitySerializer, LevelSerializer,
    SemesterSerializer, MatiereSerializer, DocumentSerializer,
    FirebaseUserSerializer, FirebaseCreateUserSerializer, AlertSerializer
)

# 🔹 Firebase
# ⚠️ Firebase est déjà initialisé automatiquement dans firebase_admin_config.py
from firebase_admin import auth as firebase_auth


# ---------------- USER ALERTS ----------------
@api_view(['GET'])
def user_alerts(request):
    user_id = request.query_params.get('user')
    if not user_id:
        return Response(
            {"error": "user parameter is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    alerts = Alert.objects.filter(user_id=user_id).order_by('-created_at')
    serializer = AlertSerializer(alerts, many=True)
    return Response(serializer.data)


# ---------------- BASE VIEWSET ----------------
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}


# ---------------- UNIVERSITY ----------------
class UniversityViewSet(BaseViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    @action(detail=True, methods=['get'], url_path='download-calendar')
    def download_calendar(self, request, pk=None):
        university = self.get_object()

        # 1️⃣ Fichier calendrier attaché au modèle
        if university.calendar and university.calendar.name:
            file_path = university.calendar.path
            if os.path.exists(file_path):
                return FileResponse(
                    open(file_path, 'rb'),
                    content_type='application/pdf'
                )

        # 2️⃣ Sinon chercher un document PDF contenant "calendrier"
        calendar_doc = Document.objects.filter(
            matiere__speciality__university=university,
            file__endswith='.pdf',
            title__icontains='calendrier'
        ).first()

        if calendar_doc and calendar_doc.file:
            return FileResponse(
                calendar_doc.file.open(),
                content_type='application/pdf'
            )

        return Response(
            {"error": "Calendrier non trouvé."},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=True, methods=['get'], url_path='calendar-url')
    def calendar_url(self, request, pk=None):
        university = self.get_object()
        if university.calendar and university.calendar.name:
            return Response({
                "url": request.build_absolute_uri(university.calendar.url)
            })

        return Response(
            {"url": None, "error": "Calendrier non trouvé."},
            status=status.HTTP_404_NOT_FOUND
        )


# ---------------- SPECIALITY ----------------
class SpecialityViewSet(BaseViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

    def get_queryset(self):
        uid = self.request.query_params.get('university_id')
        return self.queryset.filter(university_id=uid) if uid else self.queryset


# ---------------- LEVEL ----------------
class LevelViewSet(BaseViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


# ---------------- SEMESTER ----------------
class SemesterViewSet(BaseViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def get_queryset(self):
        lid = self.request.query_params.get('level_id')
        return self.queryset.filter(level_id=lid) if lid else self.queryset


# ---------------- MATIERE ----------------
class MatiereViewSet(BaseViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

    def get_queryset(self):
        filters = {}
        lev = self.request.query_params.get('level_id')
        sem = self.request.query_params.get('semester_id')
        spec = self.request.query_params.get('speciality_id')
        uid = self.request.query_params.get('university_id')

        if lev:
            filters['semester__level_id'] = lev
        if sem:
            filters['semester_id'] = sem
        if spec:
            filters['speciality_id'] = spec
        if uid:
            filters['speciality__university_id'] = uid

        return self.queryset.filter(**filters)


# ---------------- DOCUMENT ----------------
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        filters = {}
        lev = self.request.query_params.get('level_id')
        sem = self.request.query_params.get('semester_id')
        spec = self.request.query_params.get('speciality_id')
        uid = self.request.query_params.get('university_id')
        mat = self.request.query_params.get('matiere_id')

        if mat:
            filters['matiere_id'] = mat
        if sem:
            filters['matiere__semester_id'] = sem
        if lev:
            filters['matiere__semester__level_id'] = lev
        if spec:
            filters['matiere__speciality_id'] = spec
        if uid:
            filters['matiere__speciality__university_id'] = uid

        return self.queryset.filter(**filters)


# ---------------- FIREBASE ENDPOINTS ----------------
@api_view(['GET'])
def list_firebase_users(request):
    try:
        users = [
            {
                "uid": u.uid,
                "email": u.email,
                "disabled": u.disabled
            }
            for u in firebase_auth.list_users().iterate_all()
        ]
        serializer = FirebaseUserSerializer(users, many=True)
        return Response({"users": serializer.data})
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_firebase_user(request):
    serializer = FirebaseCreateUserSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        try:
            user = firebase_auth.create_user(
                email=data['email'],
                password=data['password'],
                display_name=data.get('display_name', ''),
                disabled=data.get('disabled', False)
            )
            return Response(
                {
                    "uid": user.uid,
                    "email": user.email,
                    "display_name": user.display_name,
                    "disabled": user.disabled
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
