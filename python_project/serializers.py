from rest_framework import serializers
from .models import University, Speciality, Level, Semester, Matiere, Document

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ['id', 'name', 'logo']

class SpecialitySerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)

    class Meta:
        model = Speciality
        fields = ['id', 'name', 'university', 'university_name']

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']

class SemesterSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', read_only=True)

    class Meta:
        model = Semester
        fields = ['id', 'name', 'level', 'level_name']

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
        return super().update(instance, validated_data)

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    matiere_name = serializers.CharField(source='matiere.name', read_only=True)
    semester_name = serializers.CharField(source='matiere.semester.name', read_only=True)
    level_name = serializers.CharField(source='matiere.semester.level.name', read_only=True)
    speciality_name = serializers.CharField(source='matiere.speciality.name', read_only=True)
    university_name = serializers.CharField(source='matiere.speciality.university.name', read_only=True)

    speciality_id = serializers.IntegerField(write_only=True, required=True)
    university_id = serializers.IntegerField(write_only=True, required=True)

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'file', 'file_url', 'matiere',
            'matiere_name', 'semester_name', 'level_name',
            'speciality_name', 'university_name',
            'speciality_id', 'university_id'
        ]

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        elif obj.file:
            return obj.file.url
        return None

    def validate(self, data):
        matiere = data.get('matiere')
        spec_id = data.get('speciality_id')
        uni_id = data.get('university_id')

        if matiere.speciality.id != spec_id:
            raise serializers.ValidationError("La matière ne correspond pas à la spécialité fournie.")
        if matiere.speciality.university.id != uni_id:
            raise serializers.ValidationError("La spécialité ne correspond pas à l'université fournie.")
        return data
