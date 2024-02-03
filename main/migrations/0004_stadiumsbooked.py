# Generated by Django 5.0.1 on 2024-02-02 22:26

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_stadiums_latitude_alter_stadiums_longitude'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StadiumsBooked',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('starts_time', models.DateTimeField()),
                ('ends_time', models.DateTimeField()),
                ('client', models.ForeignKey(limit_choices_to={'user_roles': 'user'}, on_delete=django.db.models.deletion.CASCADE, related_name='client_booked', to=settings.AUTH_USER_MODEL)),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stadiums_booked', to='main.stadiums')),
            ],
            options={
                'db_table': 'stadiums_booked',
            },
        ),
    ]
