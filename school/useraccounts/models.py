from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils import timezone


class MyUserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
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
            date_of_birth=date_of_birth,
            phone=phone,
            city=city,
        )
        user.superuser = False
        user.staff = False
        user.active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(
        self,
        email,
        first_name,
        last_name,
        date_of_birth,
        phone,
        city,
        password=None,
    ):
        user = self.create_user(
            email,
            first_name,
            last_name,
            date_of_birth,
            phone,
            city,
            password=password,
        )
        user.superuser = False
        user.staff = True
        user.active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email,
        first_name,
        last_name,
        date_of_birth,
        phone,
        city,
        password=None,
    ):
        user = self.create_user(
            email,
            first_name,
            last_name,
            date_of_birth,
            phone,
            city,
            password=password,
        )
        user.superuser = True
        user.staff = True
        user.active = True
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
    phone = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    picture = models.ImageField(blank=True, null=True)
    superuser = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now, blank=True, null=True)
    objects = MyUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "date_of_birth", "city"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def get_username(self):
        return self.email


new_group, created = Group.objects.get_or_create(name="Admin")
new_group1, created = Group.objects.get_or_create(name="Teacher")
new_group2, created = Group.objects.get_or_create(name="Parent")
