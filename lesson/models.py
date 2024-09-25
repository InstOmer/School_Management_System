from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class EducationTerm(models.Model):
    name =  models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    
    def __str__(self):
        return self.name

    
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    education_term = models.ForeignKey(EducationTerm, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class LessonProgram(models.Model):
    program_name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    lessons = models.ManyToManyField(Lesson, related_name="programs")
    teachers = models.ManyToManyField(User, related_name="lesson_programs")
    education_term = models.ForeignKey(EducationTerm, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return self.program_name
