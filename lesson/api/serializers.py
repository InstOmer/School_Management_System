from rest_framework import serializers
from lesson.models import Lesson, LessonProgram, EducationTerm
from student_info.api.serializers import EnrollmentSerializer
from django.contrib.auth import get_user_model


User = get_user_model()



#EducationTerm Serializer

class EducationTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationTerm
        fields = ["id", "name", "start_date", "end_date"]

# LessonSerializer

class LessonSerializer(serializers.ModelSerializer):
    enrollments = EnrollmentSerializer(source="enrollment_set", many=True, read_only=True)
    education_term = EducationTermSerializer(read_only=True)
    education_term_id = serializers.PrimaryKeyRelatedField(
        queryset=EducationTerm.objects.all(), source="education_term", write_only=True
    )
    
    class Meta:
        model = Lesson
        fields = ["id", "title", "description", "start_date", "end_date",
                  "instructor", "education_term", "education_term_id", "enrollments"]
        
        
    def create(self, validated_data):
        instructor = validated_data.get("instructor", None)
        education_term = validated_data.get("education_term", None)
        
        lesson = Lesson.objects.create(**validated_data)
        
        if instructor:
            lesson.instructor = instructor
            
        if education_term:
            lesson.education_term = education_term
            
        lesson.save()
            
        return lesson
    
    
    def update(self, instance, validated_data):
        instructor = validated_data.get("instructor", None)
        education_term = validated_data.get("education_term", None)

        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        
        if instructor is not None:
            instance.instructor = instructor
            
        if education_term is not None:
            instance.education_term = education_term
            
        instance.save()
        return instance
    
    
# LessonProgram Serailizer

class LessonProgramSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lessons_ids = serializers.PrimaryKeyRelatedField(
        queryset=Lesson.objects.all(), many=True, write_only=True, source="lessons"
    )
    education_term = EducationTermSerializer(read_only=True)
    education_term_id = serializers.PrimaryKeyRelatedField(
        queryset=EducationTerm.objects.all(), source="education_term", write_only=True
    )
    
    
    class Meta:
        model = LessonProgram
        fields = ["id", "program_name", "description", "duration", "start_date", "end_date",
                  "active", "lessons", "lessons_ids", "education_term", "education_term_id"]
        
    def create(self, validated_data):
        lessons_data = validated_data.pop("lessons", [])
        education_term = validated_data.get("education_term", None)
        lesson_program = LessonProgram.objects.create(**validated_data)
        
        if education_term:
            lesson_program.education_term = education_term
        
        if lessons_data:
            lesson_program.lessons.set(lessons_data)
            
        lesson_program.save()
            
        return lesson_program
    
    
    def update(self, instance, validated_data):
        lessons_data = validated_data.pop("lessons", [])
        education_term = validated_data.get("education_term", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if education_term is not None:
            instance.education_term = education_term
            
                    
        if lessons_data:
            instance.lessons.set(lessons_data)
                
        instance.save()
                    
        return instance