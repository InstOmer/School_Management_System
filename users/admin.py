from django.contrib import admin
from users.models import CustomUser, UserRole

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "email", "first_name", "last_name", "phone_number", "user_role", "is_active", "is_staff", "is_superuser"]
    list_display_links = ["email"]
    

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ["id", "role", "role_level"]
    list_display_links = ["role"]
