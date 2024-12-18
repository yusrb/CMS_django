# Generated by Django 5.1.1 on 2024-12-15 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_cms', '0008_alter_komunitas_boomark_alter_komunitas_deskripsi_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='komunitas',
            options={'ordering': ['nama'], 'permissions': [('can_add_konten', 'Can add konten'), ('can_change_konten', 'Can change konten'), ('can_delete_konten', 'Can delete konten'), ('can_view_konten', 'Can view konten')], 'verbose_name': 'Komunitas', 'verbose_name_plural': 'Komunitas'},
        ),
        migrations.AddField(
            model_name='konfigurasi',
            name='alamat_url',
            field=models.TextField(default='https://www.google.com/maps/place/Tugu+Pensil/@-7.8762378,110.2056043,3a,75y,352.71h,104.95t/data=!3m7!1e1!3m5!1seQaV5Ecyq0dFd3GngoCETg!2e0!6shttps:%2F%2Fstreetviewpixels-pa.googleapis.com%2Fv1%2Fthumbnail%3Fcb_client%3Dmaps_sv.tactile%26w%3D900%26h%3D600%26pitch%3D-14.95443662518835%26panoid%3DeQaV5Ecyq0dFd3GngoCETg%26yaw%3D352.7059992750229!7i16384!8i8192!4m15!1m8!3m7!1s0x2e7afb91ffc86799:0x3949bfc28dd3377b!2sTugu+Pensil!8m2!3d-7.8761448!4d110.2056676!10e5!16s%2Fg%2F11c48myyr5!3m5!1s0x2e7afb91ffc86799:0x3949bfc28dd3377b!8m2!3d-7.8761448!4d110.2056676!16s%2Fg%2F11c48myyr5?entry=ttu&g_ep=EgoyMDI0MTIxMS4wIKXMDSoASAFQAw%3D%3D'),
            preserve_default=False,
        ),
    ]
