# Generated by Django 5.1.1 on 2024-12-15 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0009_alter_komunitas_options_konfigurasi_alamat_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='konfigurasi',
            old_name='alamat_url',
            new_name='url_alamat',
        ),
    ]
