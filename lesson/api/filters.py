import django_filters
from lesson.models import Lesson, LessonProgram, EducationTerm

class LessonFilter(django_filters.FilterSet):
    instructor_email = django_filters.CharFilter(field_name="instructor__user__email", lookup_expr="icontains")
    
    class Meta:
        model = Lesson
        fields = ["start_date", "end_date", "instructor_email"]
        
        
class LessonProgramFilter(django_filters.FilterSet):
    lessons_title = django_filters.CharFilter(field_name="lesson__title", lookup_expr="icontains")
    
    class Meta:
        model = LessonProgram
        fields = ["start_date", "end_date", "active", "lessons_title"]
        
class EducationTermFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    
    class Meta:
        model = EducationTerm
        fields = ["start_date", "end_date", "name"]