# Generated by Django 4.2 on 2023-04-15 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_branch_remove_organization_group_and_more'),
        ('accounts', '0006_alter_user_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_organization', to='webapp.organization', verbose_name='Организация'),
        ),
    ]
