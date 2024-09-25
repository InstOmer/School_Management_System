from django.db import models
from django.contrib.auth import get_user_model
from lesson.models import Lesson, EducationTerm

User = get_user_model()


class StudentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)
    gpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    lessons = models.ManyToManyField(Lesson, related_name="students")
    advisorTeacher = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="advisees",
        limit_choices_to={"user_role__role": "teacher"}
    )
    
    
    def __str__(self):
        return f"{self.user.get_full_name()}"
    
    
class Enrollment(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, related_name="enrollments")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    date_enrolled = models.DateTimeField(auto_now_add=True)
    education_term = models.ForeignKey(EducationTerm, on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return f"{self.student} - {self.lesson.title}"
    
    
class Attendance(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[("present", "Present"), ("absent", "Absent")])
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.status} on {self.date}"
    
    
class Grade(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE, related_name="grades")
    subject = models.CharField(max_length=255)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.subject}: {self.score}"

