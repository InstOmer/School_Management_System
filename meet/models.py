from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meet(models.Model):
    meet_name = models.CharField(max_length=255)
    meet_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    participants = models.ManyToManyField(User, related_name="meetings", blank=True)
    
    
    def __str__(self):
        return self.meet_name
