# Generated by Django 5.1.1 on 2024-12-05 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0013_bookmarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmarks',
            name='url_link',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
    ]
