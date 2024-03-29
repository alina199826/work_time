# Generated by Django 4.2 on 2023-04-14 14:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^\\d{10}$'), django.core.validators.EmailValidator()], verbose_name='Логин'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=128, verbose_name='Пароль'),
        ),
    ]
