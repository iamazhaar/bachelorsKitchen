from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a regular User with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")  # default role for superuser

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CUSTOMER = "customer"
    ROLE_STAFF = "staff"
    ROLE_ADMIN = "admin"


    ROLE_CHOICES = [
        (ROLE_CUSTOMER, "Customer"),
        (ROLE_STAFF, "Kitchen Staff"),
        (ROLE_ADMIN, "Admin"),
    ]

    email = models.EmailField(unique=True)  # login field
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    is_staff = models.BooleanField(default=False)   # For Django admin access
    is_active = models.BooleanField(default=True)   # Can login or not
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"     # use email for authentication
    REQUIRED_FIELDS = []         # no additional fields required on createsuperuser




class Profile(models.Model):
    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),  
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        primary_key=True
    )
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    default_address = models.OneToOneField(
        "DeliveryAddress",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='default_for_profile'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class DeliveryAddress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    house = models.CharField(max_length=20)
    street = models.CharField(max_length=50)
    block = models.CharField(max_length=20, blank=True, null=True)
    area = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        profile = self.profile
        if not profile.default_address:
            profile.default_address = self
            profile.save()
