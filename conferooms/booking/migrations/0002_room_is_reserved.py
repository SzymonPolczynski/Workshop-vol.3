# Generated by Django 4.0.1 on 2022-01-19 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='is_reserved',
            field=models.BooleanField(default=False),
        ),
    ]
