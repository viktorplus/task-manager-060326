

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from apps.core.models.base import UUIDv7Model
from apps.users.choices.positions import UserPositions


class User(UUIDv7Model, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        ('username'),
        max_length=50,
        unique=True,
        error_messages={"unique": "A user with that username already exists."},
    )

    first_name = models.CharField(
        ('first name'),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )

    last_name = models.CharField(
        ('last name'),
        max_length=40,
        validators=[MinLengthValidator(2)],
    )

    email = models.EmailField(
        ('email address'),
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
    )

    phone = models.CharField(max_length=75, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(
        name="registered", auto_now_add=True
    )

    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted = models.BooleanField(default=False)
    position = models.CharField(
        max_length=15,
        choices=UserPositions.choices,
        default=UserPositions.PROGRAMMER.name
    )

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
        'position',
    ]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.deleted and self.deleted_at is None:
            self.deleted_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'