from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone
from django.core.validators import RegexValidator
from django_countries.fields import CountryField


class MyUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        country,
        date_of_birth,
        phone,
        city,
        password=None,
    ):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must provide a password")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            country=country,
            date_of_birth=date_of_birth,
            phone=phone,
            city=city,
        )
        user.is_admin = False
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        country,
        date_of_birth,
        phone,
        city,
        password=None,
    ):
        user = self.create_user(
            email,
            first_name,
            last_name,
            country,
            date_of_birth,
            phone,
            city,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r"^\+(?:[0-9]?){6,14}[0-9]$",
        message=(
            "Enter a valid international mobile phone number starting with +(country code)"
        ),
    )
    phone = models.CharField(
        validators=[phone_regex], max_length=17, blank=True, null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True, null=True)
    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone",
        "date_of_birth",
        "city",
        "country",
    ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def get_username(self):
        return self.email


# new_group, created = Group.objects.get_or_create(name="Admin")
# new_group1, created = Group.objects.get_or_create(name="Teacher")
# new_group2, created = Group.objects.get_or_create(name="Parent")
