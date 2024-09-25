from django.urls import path
from lesson.api.views import (LessonCreateView, LessonListView, LessonDetailView,
                              LessonProgramCreateView, LessonProgramListView,
                              LessonProgramDetailView, AddLessonProgramToTeacherView,
                              GetAllLessonProgramsView,GetAllLessonProgramsForTeacherView,
                              EducationTermListCreateView, EducationTermDetailView)

urlpatterns = [
    # lesson endpoints
    path("save/", LessonCreateView.as_view(), name="lesson-save"),
    path("getAll/", LessonListView.as_view(), name="lesson-list"),
    path("getAllLessonByPage/", LessonListView.as_view(), name="lesson-list-paginated"),
    path("<int:id>/", LessonDetailView.as_view(), name="lesson-detail"),
    
    # lessonprogram endpoints
    path("program/save/", LessonProgramCreateView.as_view(), name="lessonprogram-save"),
    path("program/getAll/", LessonProgramListView.as_view(), name="lessonprogram-list"),
    path("program/getAllLessonProgramByPage/", LessonProgramListView.as_view(), name="lessonprogram-list-paginate"),
    path("program/<int:id>/", LessonProgramDetailView.as_view(), name="lessonprogram-detail"),
    
    
    # admin role endpoints
    path("program/addLessonProgramToTeacher/", AddLessonProgramToTeacherView.as_view(), name="add-lesson-program-to-teacher"),
    
    # Student role endpoints
    path("program/getAllStudent/", GetAllLessonProgramsView.as_view(), name="get-all-lesson-program"),
    path("program/getAllStudentByPage/", GetAllLessonProgramsView.as_view(), name="get-all-lesson-program"),
    
    # Teacher role endpoints
    path("program/getAllTeacher/", GetAllLessonProgramsForTeacherView.as_view(), name="get-all-lesson-program-teacher"),
    path("program/getAllTeacherByPage/", GetAllLessonProgramsForTeacherView.as_view(), name="get-all-lesson-program-teacher"),
    
    # education term endpoints
    path("education-term/", EducationTermListCreateView.as_view(), name="education-term-list-create"),
    path("education-term/<int:pk>/", EducationTermDetailView.as_view(), name="education-term-detail"),
]