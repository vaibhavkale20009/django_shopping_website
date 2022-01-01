# Generated by Django 4.0 on 2021-12-31 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('desc', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('category', models.CharField(max_length=50)),
                ('stock', models.IntegerField()),
                ('disc', models.FloatField()),
                ('img', models.ImageField(upload_to='images/')),
                ('offers', models.CharField(max_length=200)),
            ],
        ),
    ]
