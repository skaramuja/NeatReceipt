# Generated by Django 3.2.18 on 2023-04-18 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20230418_1008'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='account',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='last_login',
            field=models.DateTimeField(auto_now=True, verbose_name='last login'),
        ),
    ]