from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in ["GET"]:
            return True
        
        if request.user.is_authenticated:
            if request.user.user_role.role in ["admin", "manager", "assistant_manager"]:
                return True
            
            
        return False