from django.db import models
from django.utils import timezone

from accounts.models import User
class WorkTime(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=False, blank=False,
                                 related_name="user_worktime", verbose_name="Работник")
    start_time = models.DateTimeField(auto_now=True, null=False, blank=False,  verbose_name="Дата начала")
    end_time = models.DateTimeField(auto_now=True, verbose_name="Дата конца")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания ")
    organization = models.ForeignKey('webapp.Organization', max_length=100, null=False, blank=False,
                                     related_name='org_wt', on_delete=models.CASCADE,
                                     verbose_name='Организация')

    def __str__(self):
        return f'{self.pk}. {self.user}'

class Organization(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Название")
    group = models.CharField(max_length=50, null=False, blank=False, verbose_name="Группа")
    start_time = models.DateTimeField(null=False, blank=False,  verbose_name="Дата начала")
    end_time = models.DateTimeField(verbose_name="Дата конца")
    email = models.EmailField(verbose_name="Почта")

    def __str__(self):
        return f'{self.pk}. {self.name}'

class Group(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название группы")

    def __str__(self):
        return f'{self.pk}. {self.name}'