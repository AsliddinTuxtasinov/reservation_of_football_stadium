# Generated by Django 5.0.1 on 2024-02-02 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_stadiums_latitude_alter_stadiums_longitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stadiums',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
        migrations.AlterField(
            model_name='stadiums',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9),
        ),
    ]
