# Generated by Django 5.1.1 on 2024-12-10 15:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0007_konfigurasi_favicon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='komunitas',
            name='boomark',
            field=models.ManyToManyField(blank=True, related_name='komunitas_bookmarks', to='admin_cms.bookmarks'),
        ),
        migrations.AlterField(
            model_name='komunitas',
            name='deskripsi',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='komunitas',
            name='nama',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='komunitas',
            name='peraturan',
            field=models.ManyToManyField(blank=True, related_name='komunitas_peraturan', to='admin_cms.peraturankomunitas'),
        ),
        migrations.AlterField(
            model_name='komunitas',
            name='status',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='komunitas',
            name='tanggal',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='komunitas',
            name='user',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]
