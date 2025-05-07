from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """Custom user model manager for email-based authentication. Created this to create a superuser using email"""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that uses email not username"""
    
    USER_CHOICES = [
        ('vendor', 'Vendor'),
        ('admin', 'Admin'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    user_type = models.CharField(max_length=6, choices=USER_CHOICES, default='admin')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']
    
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.id}. {self.email} : {self.user_type}"
        


# class Users(AbstractUser):
#     USER_CHOICES = [
#         ('vendor', 'Vendor'),
#         ('admin', 'Admin'),
#     ]

#     user_type = models.CharField(max_length=6, choices=USER_CHOICES, default='admin')
    
#     username = None
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(default=timezone.now)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = [] 

#     objects = CustomUserManager()


#     def __str__(self):
#         return self.email + " : " + self.user_type

