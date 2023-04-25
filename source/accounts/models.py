import uuid
from django.core.validators import RegexValidator
from django.db import models
from webapp.models import Organization
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError('The Login field must be set')
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, password, **extra_fields)


class User(AbstractBaseUser):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Фамилия")
    organization = models.ForeignKey('webapp.Organization', on_delete=models.CASCADE,
                                     related_name='user_organization',
                                     blank=False,
                                     null=False, verbose_name="Организация")
    login = models.CharField(
        max_length=13,
        validators=[RegexValidator(r'^\+996\d{9}$')],
        unique=True,
        blank=False,
        null=False,
        verbose_name="Логин"
    )
    email_verified = models.BooleanField(default=False, verbose_name="Email подтвержден")
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False,
                                                verbose_name="Токен верификации по email")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'login'

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_token", verbose_name="Работник")
    token = models.CharField(max_length=255, verbose_name="Токен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время и дата создания")
