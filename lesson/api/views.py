from rest_framework import generics, serializers
from lesson.models import Lesson, LessonProgram, EducationTerm
from lesson.api.serializers import LessonSerializer, LessonProgramSerializer, EducationTermSerializer
from django_filters.rest_framework import DjangoFilterBackend
from lesson.api.pagination import CustomPagination
from lesson.api.filters import LessonFilter, LessonProgramFilter, EducationTermFilter
from lesson.api.permissions import IsAdminUser, IsStudentUser, IsTeacherUser
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response
from school_management.permissions import IsAdminOrManagerOrAssistantManager

User = get_user_model()

# Lesson Views

class LessonCreateView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    
class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter
    
    
class LessonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    lookup_field = "id"
    
    
# lessonprogram views

class LessonProgramCreateView(generics.CreateAPIView):
    queryset = LessonProgram.objects.all()
    serializer_class = LessonProgramSerializer
    
class LessonProgramListView(generics.ListAPIView):
    queryset = LessonProgram.objects.all()
    serializer_class = LessonProgramSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonProgramFilter
    
    
    
class LessonProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonProgram.objects.all()
    serializer_class = LessonProgramSerializer
    lookup_field = "id"
    
    
class AddLessonProgramToTeacherView(generics.CreateAPIView):
    queryset = LessonProgram.objects.all()
    serializer_class = LessonProgramSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        teacher_id = self.request.data.get("teacher_id")
        
        if not teacher_id:
            raise serializers.ValidationError("Öğretmen ID'si belirtilmedi")
        
        
        try:
            teacher = User.objects.get(id=teacher_id)
            
        except User.DoesNotExist:
            raise serializers.ValidationError("Böyle bir öğretmen bulunamadı")
        
        if not teacher.is_teacher:
            raise serializers.ValidationError("Bu kullanıcı öğretmen değil")
        
        serializer.save(instructor=teacher)

class GetAllLessonProgramsView(generics.ListAPIView):
    queryset = LessonProgram.objects.all()
    serializer_class = LessonProgramSerializer
    permission_classes = [IsStudentUser]
    pagination_class = CustomPagination
    
class GetAllLessonProgramsForTeacherView(generics.ListAPIView):
    queryset = LessonProgram.objects.all()
    serializer_class = LessonProgramSerializer
    permission_classes = [IsTeacherUser]
    pagination_class = CustomPagination



class EducationTermListCreateView(generics.ListCreateAPIView):
    queryset = EducationTerm.objects.all()
    serializer_class = EducationTermSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EducationTermFilter
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    

class EducationTermDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EducationTerm.objects.all()
    serializer_class = EducationTermSerializer
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    
