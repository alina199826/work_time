# Generated by Django 4.2 on 2023-04-27 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_remove_user_organization_user_organization'),
        ('webapp', '0008_organization_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='admin',
            field=models.ManyToManyField(related_name='admin_organization', to='accounts.user'),
        ),
    ]
