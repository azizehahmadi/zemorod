from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from model_utils import FieldTracker

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, password2=None):

        if not email:
            raise ValueError('User must have an email address!')
        user = self.model(
            email=self.normalize_email(email),
            username=username,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):

        user = self.create_user(
            email,
            username=username,
            password=password
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=300,
        verbose_name='email address',
        unique=True
    )
    username = models.CharField(max_length=300)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=[('ADMIN', 'admin'), ('SELLER', 'seller'), ('BUYER', 'buyer')])
    shar = models.CharField(max_length=300)
    town = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    company = models.CharField(max_length=300, null=True, blank=True)
    address = models.TextField()
    phone = models.CharField(max_length=11)
    code_post = models.CharField(max_length=10)

    tracker = FieldTracker(fields=['role'])





