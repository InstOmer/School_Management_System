from rest_framework import permissions

class IsAdminOrManagerOrAssistantManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            
            user_role = request.user.user_role.role
            
            if user_role in ["admin", "manager", "assistant_manager"]:
                return True
        
        return False