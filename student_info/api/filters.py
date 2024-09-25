import django_filters
from student_info.models import StudentInfo, Attendance, Grade

class StudentInfoFilter(django_filters.FilterSet):
    user_email = django_filters.CharFilter(field_name="user__email", lookup_expr="icontains")
    
    class Meta:
        model = StudentInfo
        fields = ["grade", "user__email"]
        
        
class AttendanceFilter(django_filters.FilterSet):
    student_user_first_name = django_filters.CharFilter(field_name="student__user__first_name", lookup_expr="icontains")
    student_user_last_name = django_filters.CharFilter(field_name="student__user__last_name", lookup_expr="icontains")
    date = django_filters.DateFromToRangeFilter(field_name="date", lookup_expr="icontains")
    
    
    class Meta:
        model = Attendance
        fields = ["student_user_first_name", "student_user_last_name",
                  "date", "status"]
       
        
class GradeFilter(django_filters.FilterSet):
    student_user_first_name = django_filters.CharFilter(field_name="student__user__first_name", lookup_expr="icontains")
    student_user_last_name = django_filters.CharFilter(field_name="student__user__last_name", lookup_expr="icontains")
    subject = django_filters.CharFilter(field_name="subject", lookup_expr="icontains")
    score = django_filters.RangeFilter(field_name="score")
    
    
    class Meta:
        model = Grade
        fields = ["student_user_first_name", "student_user_last_name",
                  "subject", "score"]