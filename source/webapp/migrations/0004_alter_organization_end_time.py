# Generated by Django 4.2 on 2023-04-14 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_alter_organization_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата конца'),
        ),
    ]
