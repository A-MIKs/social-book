# Generated by Django 4.2.5 on 2023-09-29 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profile_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='some',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
