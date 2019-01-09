import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, first_name='', last_name='',
                    date_of_birth=None, is_active=True, is_staff=False, is_superuser=False,
                    is_seeker=False, is_employer=False):
        """ Create and save user. """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth,
            is_active = is_active,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_seeker = is_seeker,
            is_employer = is_employer,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, first_name='', last_name='',
                    date_of_birth=None):
        user = self.create_user(
            email,
            password,
            first_name = first_name,
            last_name = last_name,
            date_of_birth = date_of_birth,
            is_staff = True,
            is_superuser = True,
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User model. """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_employer = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return '{} {}.'.format(self.first_name, self.last_name[:1])
