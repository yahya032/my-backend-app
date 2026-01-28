from rest_framework import serializers
from .models import University, Speciality, Level, Semester, Matiere, Document, Alert

# ---------------- ALERT ----------------
class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'user_id', 'title', 'message', 'created_at']


# ---------------- UNIVERSITY ----------------
class UniversitySerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    calendar_url = serializers.SerializerMethodField()

    class Meta:
        model = University
        fields = ['id', 'name', 'logo_url', 'calendar_url']

    def _get_full_url(self, file_field):
        request = self.context.get('request')
        if file_field and request and file_field.name:
            url = request.build_absolute_uri(file_field.url)
            url = url.replace('127.0.0.1', '192.168.100.40').replace('localhost', '192.168.100.40')
            return url
        return None

    def get_logo_url(self, obj):
        return self._get_full_url(obj.logo)

    def get_calendar_url(self, obj):
        return self._get_full_url(obj.calendar)


# ---------------- SPECIALITY ----------------
class SpecialitySerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'university', 'university_name']


# ---------------- LEVEL ----------------
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']


# ---------------- SEMESTER ----------------
class SemesterSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', read_only=True)

    class Meta:
        model = Semester
        fields = ['id', 'name', 'level', 'level_name']


# ---------------- MATIERE ----------------
class MatiereSerializer(serializers.ModelSerializer):
    speciality_name = serializers.CharField(source='speciality.name', read_only=True)
    university_name = serializers.CharField(source='speciality.university.name', read_only=True)
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    level_name = serializers.CharField(source='semester.level.name', read_only=True)

    speciality_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Matiere
        fields = [
            'id', 'name', 'semester', 'speciality', 'speciality_id',
            'speciality_name', 'university_name', 'semester_name', 'level_name'
        ]

    def validate_speciality_id(self, value):
        if not Speciality.objects.filter(id=value).exists():
            raise serializers.ValidationError("La spécialité spécifiée n'existe pas.")
        return value

    def create(self, validated_data):
        speciality_id = validated_data.pop('speciality_id')
        validated_data['speciality'] = Speciality.objects.get(id=speciality_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'speciality_id' in validated_data:
            speciality_id = validated_data.pop('speciality_id')
            instance.speciality = Speciality.objects.get(id=speciality_id)
            instance.save()
        return super().update(instance, validated_data)


# ---------------- DOCUMENT ----------------
class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    matiere_name = serializers.CharField(source='matiere.name', read_only=True)
    semester_name = serializers.CharField(source='matiere.semester.name', read_only=True)
    level_name = serializers.CharField(source='matiere.semester.level.name', read_only=True)
    speciality_name = serializers.CharField(source='matiere.speciality.name', read_only=True)
    university_name = serializers.CharField(source='matiere.speciality.university.name', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file', 'file_url', 'matiere',
            'matiere_name', 'semester_name', 'level_name',
            'speciality_name', 'university_name'
        ]

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request and obj.file.name:
            url = request.build_absolute_uri(obj.file.url)
            url = url.replace('127.0.0.1', '192.168.100.40').replace('localhost', '192.168.100.40')
            return url
        return None

    def validate(self, data):
        if not data.get('matiere'):
            raise serializers.ValidationError({"matiere": "Matière obligatoire."})
        return data


# ---------------- FIREBASE SERIALIZERS ----------------
class FirebaseUserSerializer(serializers.Serializer):
    uid = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    disabled = serializers.BooleanField()


class FirebaseCreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    display_name = serializers.CharField(required=False, allow_blank=True)
    disabled = serializers.BooleanField(default=False)
