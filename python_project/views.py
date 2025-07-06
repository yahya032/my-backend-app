from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import University, Speciality, Level, Semester, Matiere, Document
from .serializers import (
    UniversitySerializer, SpecialitySerializer, LevelSerializer,
    SemesterSerializer, MatiereSerializer, DocumentSerializer
)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Veuillez fournir un nom d\'utilisateur et un mot de passe'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Identifiants invalides'}, status=status.HTTP_401_UNAUTHORIZED)

class UniversityViewSet(viewsets.ModelViewSet):
    queryset = University.objects.all()
    serializer_class = UniversitySerializer

class SpecialityViewSet(viewsets.ModelViewSet):
    queryset = Speciality.objects.all()
    serializer_class = SpecialitySerializer

    def get_queryset(self):
        uid = self.request.query_params.get('university_id')
        if uid:
            return Speciality.objects.filter(university_id=uid)
        return Speciality.objects.all()

class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class SemesterViewSet(viewsets.ModelViewSet):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def get_queryset(self):
        lid = self.request.query_params.get('level_id')
        if lid:
            return Semester.objects.filter(level_id=lid)
        return Semester.objects.all()

class MatiereViewSet(viewsets.ModelViewSet):
    queryset = Matiere.objects.all()
    serializer_class = MatiereSerializer

    def get_queryset(self):
        qs = Matiere.objects.all()
        lev = self.request.query_params.get('level_id')
        sem = self.request.query_params.get('semester_id')
        spec = self.request.query_params.get('speciality_id')
        uid = self.request.query_params.get('university_id')

        if lev:
            qs = qs.filter(semester__level_id=lev)
        if sem:
            qs = qs.filter(semester_id=sem)
        if spec:
            qs = qs.filter(speciality_id=spec)
        if uid:
            qs = qs.filter(speciality__university_id=uid)
        return qs

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        qs = super().get_queryset()
        uid = self.request.query_params.get('university_id')
        spec = self.request.query_params.get('speciality_id')
        lev = self.request.query_params.get('level_id')
        sem = self.request.query_params.get('semester_id')
        mat = self.request.query_params.get('matiere_id')

        if mat:
            qs = qs.filter(matiere_id=mat)
        if sem:
            qs = qs.filter(matiere__semester_id=sem)
        if lev:
            qs = qs.filter(matiere__semester__level_id=lev)
        if spec:
            qs = qs.filter(matiere__speciality_id=spec)
        if uid:
            qs = qs.filter(matiere__speciality__university_id=uid)
        return qs
