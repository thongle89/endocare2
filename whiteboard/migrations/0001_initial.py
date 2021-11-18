# Generated by Django 3.2.6 on 2021-11-17 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_e', models.IntegerField(choices=[(1, 'Bảo trì'), (2, 'Training')], default=1, verbose_name='Type')),
                ('name', models.CharField(max_length=120, verbose_name='Event Name')),
                ('event_date', models.DateTimeField(verbose_name='Event Date')),
                ('description', models.TextField(blank=True)),
                ('attendees', models.ManyToManyField(blank=True, related_name='attendees', to=settings.AUTH_USER_MODEL)),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manager', to='home.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cmt_time', models.DateTimeField(auto_now_add=True)),
                ('cmt_text', models.TextField(verbose_name='Nội dung')),
                ('is_verified', models.BooleanField(blank=True, null=True, verbose_name='Xác Nhận')),
                ('verifier', models.CharField(blank=True, max_length=50, null=True, verbose_name='Người xác nhận')),
                ('verify_time', models.DateTimeField(blank=True, null=True, verbose_name='Ngày xác nhận')),
                ('rma_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.exfm')),
                ('username', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
