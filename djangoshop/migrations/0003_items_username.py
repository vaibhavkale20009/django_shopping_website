# Generated by Django 4.0 on 2022-01-01 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoshop', '0002_cartdb'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='username',
            field=models.CharField(default='vaibhav', max_length=20),
            preserve_default=False,
        ),
    ]
