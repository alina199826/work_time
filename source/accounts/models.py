from django.core.validators import RegexValidator
from django.db import models

# #
# from webapp.models import Organization


class User(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Имя")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Фамилия")
    # organization = models.ForeignKey('webapp.Organization', on_delete=models.CASCADE, default=1,
    #                                  related_name='user_organization',
    #                                  blank=False,
    #                                  null=False, verbose_name="Организация")
    login = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^\d{10}$')],
        unique=True,
        blank=False,
        null=False,
        verbose_name="Логин"
    )
    password = models.CharField(max_length=128, blank=False, null=False, verbose_name="Пароль")


    def __str__(self):
        return f"{self.name} "
