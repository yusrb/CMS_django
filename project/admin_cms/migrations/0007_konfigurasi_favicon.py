# Generated by Django 5.1.1 on 2024-12-10 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0006_bookmarks_komunitas_peraturankomunitas_komunitas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='konfigurasi',
            name='favicon',
            field=models.ImageField(null=True, upload_to='favicon_foto/'),
        ),
    ]
