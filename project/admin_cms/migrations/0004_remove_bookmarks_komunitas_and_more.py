# Generated by Django 5.1.1 on 2024-12-10 10:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0003_remove_kategori_foto_alter_konfigurasi_iklan_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmarks',
            name='komunitas',
        ),
        migrations.RemoveField(
            model_name='peraturankomunitas',
            name='komunitas',
        ),
        migrations.AddField(
            model_name='komunitas',
            name='boomark',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_cms.bookmarks'),
        ),
        migrations.AddField(
            model_name='komunitas',
            name='peraturan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_cms.peraturankomunitas'),
        ),
    ]
