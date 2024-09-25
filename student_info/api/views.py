from rest_framework import generics
from student_info.models import StudentInfo, Attendance, Enrollment, Grade
from student_info.api.serializers import StudentInfoSerializer, AttendanceSerializer, GradeSerializer, EnrollmentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from school_management.permissions import IsAdminOrManagerOrAssistantManager
from student_info.api.pagination import CustomPagination
from student_info.api.filters import StudentInfoFilter, AttendanceFilter, GradeFilter
from student_info.api.permissions import IsAdminOrReadOnly

# StudentInfo Create View

class StudentInfoCreateView(generics.CreateAPIView):
    queryset = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    
    
class StudentInfoListView(generics.ListAPIView):
    queryset = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentInfoFilter
    
    
class StudentInfoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentInfo.objects.all()
    serializer_class = StudentInfoSerializer
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    
    
class AttendanceCreateView(generics.CreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    
class AttendanceListView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AttendanceFilter
    
    
class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    
    
class GradeCreateView(generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    
    
    
class GradeListView(generics.ListAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = GradeFilter
    
    
class GradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAdminOrManagerOrAssistantManager]
    
    
class EnrollmentListCreateView(generics.ListCreateAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    
class EnrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdminOrReadOnly]