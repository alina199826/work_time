from django.contrib.auth import get_user_model
from django.db import models


class User(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='user', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    organization = models.ForeignKey('webapp.Organization', max_length=100, on_delete=models.CASCADE, null=False, blank=False,
                                     verbose_name='Организация')

