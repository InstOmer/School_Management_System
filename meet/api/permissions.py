from rest_framework.permissions import BasePermission

class IsAdminOrTeacherOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        
        
        if request.method in ["GET"] and user.is_authenticated and user.user_role.role in ["student", "manager", "assistant_manager"]:
            return True
        
        
        if user.is_authenticated:
            if user.user_role.role in ["admin", "teacher"]:
                return True
            
        return False