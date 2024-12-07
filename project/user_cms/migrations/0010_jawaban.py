# Generated by Django 5.1.1 on 2024-12-07 04:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_cms', '0009_alter_pertanyaan_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Jawaban',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isi', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('penulis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('pertanyaan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jawaban', to='user_cms.pertanyaan')),
            ],
            options={
                'verbose_name': 'Jawaban Pertanyaan',
                'verbose_name_plural': 'Jawaban Pertanyaan',
            },
        ),
    ]