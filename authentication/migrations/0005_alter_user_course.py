# Generated by Django 5.0.4 on 2024-06-01 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_department_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='authentication.course'),
        ),
    ]
