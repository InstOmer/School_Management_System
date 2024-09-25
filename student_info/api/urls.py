from django.urls import path
from student_info.api.views import (StudentInfoCreateView, StudentInfoListView,
                                    StudentInfoDetailView, AttendanceCreateView,
                                    AttendanceListView, AttendanceDetailView,
                                    GradeCreateView, GradeListView, GradeDetailView,
                                    EnrollmentListCreateView, EnrollmentDetailView)

urlpatterns = [
    path("save/", StudentInfoCreateView.as_view(), name="studentinfo-save"),
    path("getAll/", StudentInfoListView.as_view(), name="studentinfo-list"),
    path("getAllStudentInfoByPage/", StudentInfoListView.as_view(), name="studentinfo-list-paginate"),
    path("<int:pk>/", StudentInfoDetailView.as_view(), name="studentinfo-detail"),
    
    # attendance urls
    path("attendance/save/", AttendanceCreateView.as_view(), name="attendance-create"),
    path("attendance/getAll/", AttendanceListView.as_view(), name="attendance-list"),
    path("attendance/getAllAttendanceByPage/", AttendanceListView.as_view(), name="attendance-list-paginate"),
    path("attendance/<int:pk>/", AttendanceDetailView.as_view(), name="attendance-detail"),
   
    # grade urls
    path("grade/save/", GradeCreateView.as_view(), name="grade-create"),
    path("grade/getAll/", GradeListView.as_view(), name="grade-list"),
    path("grade/getAllGradeByPage/", GradeListView.as_view(), name="grade-list-paginate"),
    path("grade/<int:pk>/", GradeDetailView.as_view(), name="grade-detail"),
    
    path("enrollments/", EnrollmentListCreateView.as_view(), name="enrollment-list-create"),
    path("enrollments/<int:pk>/", EnrollmentDetailView.as_view(), name="enrollment-detail"),
   
]