from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.utils.crypto import get_random_string
# create permissions for group



# create user and superuser
# class MyUserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def create_user(self, email, password, **extra_fields):
#         email = self.normalize_email(email)
#         user = self.model(email=email)
#         user.set_password(password)
#         user.create_activation_code()
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         email = self.normalize_email(email)
#         user = self.model(email=email)
#         user.set_password(password)
#         user.is_active = True
#         user.is_stuff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user
class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class MyUser(AbstractUser):
    username = None
    # first_name = models.CharField(max_length=150, blank=True)
    # last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def create_activation_code(self):
        code = get_random_string(length=20,
                                 allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        self.activation_code = code

# create group

