from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class UserRole(models.Model):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'
    MANAGER = 'manager'
    ASSISTANT_MANAGER = 'assistant_manager'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (STUDENT, 'Student'),
        (MANAGER, 'Manager'),
        (ASSISTANT_MANAGER, 'Assistant Manager'),
    ]

    role = models.CharField(_('role'), max_length=20, choices=ROLE_CHOICES, default=STUDENT)
    role_level = models.IntegerField(editable=False)
    
    def save(self, *args, **kwargs):
        if self.role == self.ADMIN:
            self.role_level = 1
        elif self.role == self.MANAGER:
            self.role_level = 2
        elif self.role == self.ASSISTANT_MANAGER:
            self.role_level = 3
        elif self.role == self.TEACHER:
            self.role_level = 4
        elif self.role == self.STUDENT:
            self.role_level = 5
            
        super(UserRole, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_role_display()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Email alanı zorunludur'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(
        regex=r"^\(\d{3}\) \d{3}-\d{4}$",
        message="Phone number must be entered in the format: (999) 999-9999"
    )
    
    email = models.EmailField(_('email address'), unique=True, help_text=_('Kullanıcının e-posta adresi'))
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    phone_number = models.CharField(_('phone number'), validators=[phone_regex], max_length=14, blank=True, null=True)
    address = models.CharField(_('address'), max_length=100, blank=True, null=True)
    zip_code = models.CharField(_('zip code'), max_length=10, blank=True, null=True)

    
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)
    
    user_role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True, blank=True)
    

    # Çakışmayı önlemek için related_name ekleniyor
    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='customuser_user_permissions', blank=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    
    def save(self, *args, **kwargs):
        if self.user_role:
            if self.user_role.role == UserRole.ADMIN:
                self.is_superuser = True
                self.is_staff = True
            elif self.user_role.role in [UserRole.MANAGER, UserRole.ASSISTANT_MANAGER]:
                self.is_staff = True
                self.is_superuser = False
            else:
                self.is_staff = False
                self.is_superuser = False
        super().save(*args, **kwargs)