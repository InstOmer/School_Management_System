from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import UserRole

User = get_user_model()


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ["role"]
        
        
class UserSerializer(serializers.ModelSerializer):
    user_role = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all())
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone_number", "address", "zip_code", "user_role"]
        
        
    def update(self, instance, validated_data):
        user_role_data = validated_data.pop("user_role", None)
        
        if user_role_data:
            request_user = self.context["request"].user
            
            current_user_role_level = request_user.user_role.role_level

            new_user_role_level = user_role_data.role_level
            
            if new_user_role_level < current_user_role_level:
                raise serializers.ValidationError("Kullanıcı, kendisinden daha yüksek seviyede bir rol atayamaz.")
            
            
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.address = validated_data.get("address", instance.address)
        instance.zip_code = validated_data.get("zip_code", instance.zip_code)
        instance.save()
        
        
        if user_role_data:
            instance.user_role = user_role_data
            instance.save()
            
        return instance
        
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    user_role_detail = UserRoleSerializer(read_only=True, source="user_role")
    
    
    class Meta:
        model = User
        fields = ["email", "password", "confirm_password", "first_name", "last_name", "user_role_detail"]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True},
        }
        
        
    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        
        if password != confirm_password:
            raise serializers.ValidationError("Şifreler eşleşmiyor.")
        
        return data
    
    def create(self, validated_data):
        validated_data.pop("confirm_password")
        
        
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", "")
        )
        
        student_role = UserRole.objects.get(role="student")
        user.user_role = student_role
        user.save()
        
        return user
    
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField()
    
    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        
        if email and password:
            user = authenticate(request=self.context.get("request"), email=email, password=password)
            
            if user is None:
                raise serializers.ValidationError("E-posta veya şifre yanlış!")
            
            if not user.is_active:
                raise serializers.ValidationError("Bu hesap aktif değil.")
            
        else:
            raise serializers.ValidationError("E-posta ve şifre alanları zorunludur.")
        
        refresh = RefreshToken.for_user(user)
        
        return {
            "refresh" : str(refresh),
            "access": str(refresh.access_token),
            "user": self.get_user(user)
        }
        
        
    def get_user(self, user):
        return {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_role": user.user_role.role if user.user_role else None
        }
        
        
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    
    def validate_new_password(self, value):
        validate_password(value)
        return value
    
    def validate(self, data):
        user = self.context["request"].user
        
        if not user.check_password(data["old_password"]):
            raise serializers.ValidationError("Eski şifre yanlış")
        
        return data
    
    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
    
    
    
class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "address", "zip_code"]
        
        
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.address = validated_data.get("address", instance.address)
        instance.zip_code = validated_data.get("zip_code", instance.zip_code)
        instance.save()
        return instance
    
    
class UserFilterSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate(self, data):
        if not data.get('first_name') and not data.get('last_name'):
            raise serializers.ValidationError("En az bir arama kriteri belirtmelisiniz (first_name veya last_name).")
        return data