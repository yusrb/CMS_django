# Generated by Django 5.1.1 on 2024-12-15 17:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_cms', '0003_alter_konten_isi_konten'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Galeri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_link', models.CharField(max_length=60)),
                ('foto', models.ImageField(upload_to='galeri_foto/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Galeri',
                'verbose_name_plural': 'Galeri',
            },
        ),
    ]
