# Generated by Django 3.2.13 on 2022-05-13 03:52

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_company_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='company_id',
            field=models.CharField(blank=True, max_length=12, validators=[accounts.models.validate_company_id]),
        ),
    ]
