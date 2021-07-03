  
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from django.utils.translation import ugettext_lazy as _




import uuid




# phone_regex = r'\d.+{13}'


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)




class User(AbstractUser):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=255)
    
    date_joined = models.DateField(auto_now_add=True)
    
    username = None

    objects = CustomUserManager()


    REQUIRED_FIELDS = ('name', 'phone_number',)
    USERNAME_FIELD = 'email'



    def __str__(self):
        return (f'{self.name} ({self.email})')