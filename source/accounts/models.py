import uuid

from django.core.validators import RegexValidator
from django.db import models
from webapp.models import Organization


class User(models.Model):
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
    password = models.CharField(max_length=128, blank=False, null=False, verbose_name="Пароль")
    email_verified = models.BooleanField(default=False, verbose_name="Email подтвержден")
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False,
                                                verbose_name="Токен верификации по email")


    def __str__(self):
        return f"{self.name} "


class VerificationToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_token", verbose_name="Работник")
    token = models.CharField(max_length=255, verbose_name="Токен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время и дата создания")
