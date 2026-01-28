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
from firebase_admin import auth as firebase_auth

# ================== ALERTS ==================
@api_view(['GET'])
def user_alerts(request):
    user_id = request.query_params.get('user')
    if not user_id:
        return Response({"error": "user parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    alerts = Alert.objects.filter(user_id=user_id).order_by('-created_at')
    serializer = AlertSerializer(alerts, many=True)
    return Response(serializer.data)

# ================== BASE VIEWSET ==================
class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

# ================== UNIVERSITY ==================
class UniversityViewSet(BaseViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

    @action(detail=True, methods=['get'], url_path='download-calendar')
    def download_calendar(self, request, pk=None):
        university = self.get_object()

        if university.calendar and university.calendar.name:
            file_path = university.calendar.path
            if os.path.exists(file_path):
                return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

        # fallback: chercher un document PDF nommé "calendrier"
        calendar_doc = Document.objects.filter(
            matiere__speciality__university=university,
            file__endswith='.pdf',
            title__icontains='calendrier'
        ).first()

        if calendar_doc and calendar_doc.file:
            return FileResponse(calendar_doc.file.open(), content_type='application/pdf')

        return Response({"error": "Calendrier non trouvé."}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='calendar-url')
    def calendar_url(self, request, pk=None):
        university = self.get_object()
        if university.calendar and university.calendar.name:
            return Response({"url": request.build_absolute_uri(university.calendar.url)})
        return Response({"url": None, "error": "Calendrier non trouvé."}, status=status.HTTP_404_NOT_FOUND)

# ================== SPECIALITY ==================
class SpecialityViewSet(BaseViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

    def get_queryset(self):
        university_id = self.request.query_params.get('university_id')
        if university_id:
            return self.queryset.filter(university_id=university_id)
        return self.queryset

# ================== LEVEL ==================
class LevelViewSet(BaseViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

# ================== SEMESTER ==================
class SemesterViewSet(BaseViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def get_queryset(self):
        level_id = self.request.query_params.get('level_id')
        if level_id:
            return self.queryset.filter(level_id=level_id)
        return self.queryset

# ================== MATIERE ==================
class MatiereViewSet(BaseViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

    def get_queryset(self):
        filters = {}
        level_id = self.request.query_params.get('level_id')
        semester_id = self.request.query_params.get('semester_id')
        speciality_id = self.request.query_params.get('speciality_id')
        university_id = self.request.query_params.get('university_id')

        if level_id:
            filters['level_id'] = level_id           # 🔹 Filtrage direct sur level
        if semester_id:
            filters['semester_id'] = semester_id
        if speciality_id:
            filters['speciality_id'] = speciality_id
        if university_id:
            filters['speciality__university_id'] = university_id

        return self.queryset.filter(**filters)

# ================== DOCUMENT ==================
class DocumentViewSet(BaseViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        filters = {}
        level_id = self.request.query_params.get('level_id')
        semester_id = self.request.query_params.get('semester_id')
        speciality_id = self.request.query_params.get('speciality_id')
        university_id = self.request.query_params.get('university_id')
        matiere_id = self.request.query_params.get('matiere_id')

        if matiere_id:
            filters['matiere_id'] = matiere_id
        if semester_id:
            filters['matiere__semester_id'] = semester_id
        if level_id:
            filters['matiere__level_id'] = level_id        # 🔹 level direct
        if speciality_id:
            filters['matiere__speciality_id'] = speciality_id
        if university_id:
            filters['matiere__speciality__university_id'] = university_id

        return self.queryset.filter(**filters)

# ================== FIREBASE ==================
@api_view(['GET'])
def list_firebase_users(request):
    try:
        users = [{"uid": u.uid, "email": u.email, "disabled": u.disabled}
                 for u in firebase_auth.list_users().iterate_all()]
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
            return Response({
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "disabled": user.disabled
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
