# Generated by Django 3.2.6 on 2021-09-22 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210920_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='pending',
            name='superadmin',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Super Admin'),
        ),
    ]
