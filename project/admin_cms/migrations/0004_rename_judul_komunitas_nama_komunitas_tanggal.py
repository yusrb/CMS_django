# Generated by Django 5.1.1 on 2024-11-27 06:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0003_komunitas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='komunitas',
            old_name='judul',
            new_name='nama',
        ),
        migrations.AddField(
            model_name='komunitas',
            name='tanggal',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
