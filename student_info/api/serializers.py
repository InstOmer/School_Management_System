from rest_framework import serializers
from student_info.models import StudentInfo, Enrollment, Attendance, Grade
from django.contrib.auth import get_user_model
from lesson.models import Lesson, EducationTerm

User = get_user_model()

# StudentInfo Serializer

class StudentInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.CharField(source="user.email")
    phone_number = serializers.CharField(source="user.phone_number")
    
    user_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = StudentInfo
        fields = ["id", "first_name", "last_name", "email", "phone_number", 
                  "grade", "gpa", "user_id", "advisorTeacher"]
        
        
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")
        phone_number = user_data.get("phone_number")
        
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"first_name": first_name, "last_name": last_name, "phone_number": phone_number}
        )
        
        student_info = StudentInfo.objects.create(user=user, **validated_data)
        
        return student_info
    
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        
        first_name = user_data.get("first_name")
        last_name = user_data.get("last_name")
        email = user_data.get("email")
        phone_number = user_data.get("phone_number")
        
        if first_name:
            instance.user.first_name = first_name
        
        if last_name:
            instance.user.last_name = last_name
            
        if email:
            instance.user.email = email
            
        if phone_number:
            instance.user.phone_number = phone_number
            
            
        instance.user.save()
        
        instance.grade = validated_data.get("grade", instance.grade)
        instance.gpa = validated_data.get("gpa", instance.gpa)
        instance.save()
        
        return instance
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    def get_last_name(self, obj):
        return obj.user.last_name
    
    def get_email(self, obj):
        return obj.user.email
    
    def get_phone_number(self, obj):
        return obj.user.phone_number
    


# Enrollment Serializer

class EnrollmentSerializer(serializers.ModelSerializer):
    student_id = serializers.PrimaryKeyRelatedField(
        queryset = StudentInfo.objects.all(), source="student", write_only=True
    )
    lesson_id = serializers.PrimaryKeyRelatedField(
        queryset = Lesson.objects.all(), source="lesson", write_only=True
    )
    education_term_id = serializers.PrimaryKeyRelatedField(
        queryset = EducationTerm.objects.all(), source="education_term", write_only=True
    )
    
    class Meta:
        model = Enrollment
        fields = ["student", "student_id", "lesson", "lesson_id", "date_enrolled", 
                  "education_term", "education_term_id"]
        
    def create(self, validated_data):
        student = validated_data.get("student")
        lesson = validated_data.get("lesson")
        education_term = validated_data.get("education_term")
        
        enrollment = Enrollment.objects.create(
            student=student,
            lesson=lesson,
            education_term=education_term
        )
        
        return enrollment
        
        
# Attandance Serializer

class AttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=StudentInfo.objects.all())

    class Meta:
        model = Attendance
        fields = ["id", "student", "date", "status"]
        
        
        
# Grade Serializer

class GradeSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=StudentInfo.objects.all())

    class Meta:
        model = Grade
        fields = ["id", "student", "subject", "score"]