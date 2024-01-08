import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):

    def create_user(self, phone, password):
        if not phone:
            raise ValueError('User must have a phone')

        user = self.model(phone=phone)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone, password, is_superuser=True):
        if not phone:
            raise ValueError('User must have a phone')

        user = self.model(phone=phone, is_superuser=is_superuser,
                          is_staff=True, is_active=True, is_confirmed=True)
        user.first_name = 'admin'
        user.last_name = 'admin'
        user.set_password(password)
        user.save()

        return user


class UserAccounts(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    patronymic_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)

    objects = UserManager()

    is_active = models.BooleanField(blank=True, default=False)
    is_confirmed = models.BooleanField(default=False)
    in_consideration = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []
