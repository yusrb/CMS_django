# Generated by Django 5.1.1 on 2024-12-05 14:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0010_alter_galeri_options_alter_kategori_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='komunitas',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]