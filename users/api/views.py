from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from users.api.permissions import IsSuperUser
from rest_framework.exceptions import PermissionDenied
from users.api.serializers import (
    RegisterSerializer, LoginSerializer, ChangePasswordSerializer,
    UpdateProfileSerializer, UserSerializer, UserFilterSerializer
)
from django.contrib.auth import get_user_model
from users.models import UserRole
from school_management.permissions import IsAdminOrManagerOrAssistantManager
import logging

User = get_user_model()

logger = logging.getLogger(__name__)




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return User.objects.none()
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        
        return Response({
            "user": RegisterSerializer(user).data,
            "refresh": str(refresh),
            "access": str(access)
        })
        
        
        
        
class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)
    
    
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]
    
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message": "Şifre başarıyla güncellendi."
        }, status=status.HTTP_200_OK)
        
        
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    
class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            # Kullanıcılar kendi detaylarını görebilir veya rolüne göre başka kullanıcıların detaylarını görebilir.
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        
        if user.user_role.role == UserRole.ADMIN:
            # Admin tüm kullanıcıları görebilir
            return User.objects.all()
        
        elif user.user_role.role in [UserRole.MANAGER, UserRole.ASSISTANT_MANAGER]:
            # Manager ve Assistant Manager sadece Teacher ve Student'ları görebilir
            return User.objects.filter(user_role__role__in=[UserRole.TEACHER, UserRole.STUDENT])
        
        else:
            # Student ve Teacher sadece kendi verilerini görebilir
            return User.objects.filter(id=user.id)

    def get_object(self):
        user = self.request.user
        
        obj = super().get_object()
        # Admin ise herhangi bir kullanıcıya erişebilir
        if user.user_role.role == UserRole.ADMIN:
            return obj
        

        # Manager ve Assistant Manager sadece Teacher ve Student'lara erişebilir
        if user.user_role.role in [UserRole.MANAGER, UserRole.ASSISTANT_MANAGER]:
            obj = super().get_object()
            if obj.user_role.role not in [UserRole.TEACHER, UserRole.STUDENT] and obj != user:
                raise PermissionDenied("Sadece Teacher ve Student kullanıcılarına erişebilirsiniz.")
            return obj
        
        # Student ve Teacher sadece kendi verilerine erişebilir
        if user.user_role.role in [UserRole.TEACHER, UserRole.STUDENT]:
            if obj != user:
                raise PermissionDenied("Sadece kendi verilerinize erişebilirsiniz.")
            return obj

        raise PermissionDenied("Erişim izniniz yok.")

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        current_user = request.user

        # Kullanıcı kendi hesabını silemez
        if current_user == user:
            return Response(
                {
                    'error': 'Kendi hesabınızı silemezsiniz.',
                    'details': 'Kendi kullanıcı hesabınızı silmeye çalışıyorsunuz, bu işlem güvenlik nedeniyle engellenmiştir.'
                }, 
                status=status.HTTP_403_FORBIDDEN
            )

        # Admin ise herhangi bir kullanıcıyı silebilir
        if current_user.user_role.role == UserRole.ADMIN:
            return super().destroy(request, *args, **kwargs)
        
        # Manager ve Assistant Manager sadece Teacher ve Student'ları silebilir
        if current_user.user_role.role in [UserRole.MANAGER, UserRole.ASSISTANT_MANAGER]:
            if user.user_role.role not in [UserRole.TEACHER, UserRole.STUDENT]:
                return Response(
                    {
                        'error': 'Bu kullanıcıyı silemezsiniz.',
                        'details': 'Sadece Teacher ve Student kullanıcılarını silebilirsiniz.'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )
            return super().destroy(request, *args, **kwargs)

        # Student ve Teacher kimseyi silemez
        return Response(
            {
                'error': 'Silme izniniz yok.',
                'details': 'Bu işlem için yetkiniz yok.'
            },
            status=status.HTTP_403_FORBIDDEN
        )
    
    
class GetUserByNameView(generics.GenericAPIView):
    permission_classes = [IsSuperUser]
    serializer_class = UserFilterSerializer
    queryset = User.objects.all()
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        if user.user_role.role != UserRole.ADMIN:
            return Response(
                {
                    "detail": "Bu işlem için yetkiniz yok."
                },
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        first_name = serializer.validated_data.get("first_name")
        last_name = serializer.validated_data.get("last_name")
        
        queryset = self.get_queryset()
        
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
            
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
            
            
        user_serializer = UserSerializer(queryset, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    
class UserListAll(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsSuperUser]