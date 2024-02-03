# Generated by Django 5.0.1 on 2024-02-02 21:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadiums',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='stadiums',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='stadiums',
            name='owner',
            field=models.ForeignKey(limit_choices_to={'user_roles': 'stadium owner'}, on_delete=django.db.models.deletion.CASCADE, related_name='stadiums', to=settings.AUTH_USER_MODEL),
        ),
    ]
