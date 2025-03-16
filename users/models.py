from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.text import slugify

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password,**extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email).lower()
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password,**extra_fields):
        user = self.create_user(email,password,**extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    full_name = models.CharField(max_length=125)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=200,null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    slug = models.SlugField(max_length=255,blank=True,unique=True)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    def save(self,*args, **kwargs):
        if not self.slug:
            title =  self.full_name + self.email
            self.slug = slugify(title)
        super().save(*args, **kwargs)
        pass
