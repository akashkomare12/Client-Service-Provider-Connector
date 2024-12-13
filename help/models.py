from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

class ClientManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        
        # Ensure to call set_password to hash the password before saving
        if password:
            password = make_password(password)
            user.set_password(password)
            print(password)
        
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class Client(AbstractBaseUser, PermissionsMixin):
    client_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='client_groups', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='client_permissions', 
        blank=True
    )

    objects = ClientManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

#Service Provider 
class ServiceProviderManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        
        # Ensure to call set_password to hash the password before saving
        if password:
            user.set_password(password)
        
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)

class ServiceProvider(AbstractBaseUser, PermissionsMixin):
    sp_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    password = models.CharField(max_length=128)
    mobile = models.CharField(max_length=15, unique=True)
    skills = models.CharField(max_length=20, choices=[
        ('plumber', 'Plumber'),
        ('cleaner', 'Cleaner'),
        ('electrician', 'Electrician'),
        ('cook', 'Cook'),
    ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='service_provider_groups',  # Add unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='service_provider_permissions',  # Add unique related_name
        blank=True
    )

    objects = ServiceProviderManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return f"{self.sp_id} {self.name}"
    

class ServiceRecords(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    u_id = models.ForeignKey(Client, on_delete=models.CASCADE)  # Relates to Django's Client model
    sp_id = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)  # Relates to ServiceProvider
    service = models.CharField(max_length=200)  # Service description
    date = models.DateTimeField()  # Date and time of service
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount charged for the service
    ratings = models.PositiveSmallIntegerField(null=True, blank=True)  # Ratings (1-5), optional
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Service status

    def __str__(self):
        return f"Service {self.service} by {self.sp_id.name} for User {self.u_id.username}"