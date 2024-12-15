from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import os
from admin_cms.models import User, Aktivitas
from user_cms.models import Konten, Galeri

@receiver(post_save, sender=Konten)
def log_konten_save(sender, instance, created, **kwargs):
    user = instance.user
    aksi = f'Menambahkan Konten: {instance.judul}' if created else f'Mengubah Konten: {instance.judul}'

    try:
        user_instance = User.objects.get(username=user.username)
        Aktivitas.objects.create(user=user_instance, aksi=aksi)

        # Handle foto update saat update konten
        if not created:
            if instance.pk:
                old_instance = Konten.objects.get(pk=instance.pk)
                # Cek jika foto lama berbeda dengan foto baru
                if old_instance.foto != instance.foto:
                    if old_instance.foto:
                        old_foto_path = old_instance.foto.path
                        # Pastikan foto lama ada dan berbeda dengan foto baru
                        if os.path.exists(old_foto_path) and old_foto_path != instance.foto.path:
                            os.remove(old_foto_path)
                    # Tidak perlu memeriksa foto baru, foto baru sudah disimpan saat update

    except ObjectDoesNotExist:
        print(f"User with username {user.username} does not exist.")

@receiver(post_delete, sender=Konten)
def log_konten_delete(sender, instance, **kwargs):
    user = instance.user
    aksi = f'Menghapus Konten: {instance.judul}'

    try:
        user_instance = User.objects.get(username=user.username)
        Aktivitas.objects.create(user=user_instance, aksi=aksi)

        # Hapus foto saat konten dihapus
        if instance.foto:
            foto_path = instance.foto.path
            if os.path.exists(foto_path):
                os.remove(foto_path)
    except ObjectDoesNotExist:
        print(f"User with username {user.username} does not exist.")

@receiver(post_save, sender=Galeri)
def log_galeri_save(sender, instance, created, **kwargs):
    user = instance.user
    aksi = f'Menambahkan Galeri: {instance.url_link}' if created else f'Mengubah Galeri: {instance.url_link}'

    try:
        user_instance = User.objects.get(username=user.username)
        Aktivitas.objects.create(user=user_instance, aksi=aksi)

        # Handle foto update saat update galeri
        if not created:
            if instance.pk:
                old_instance = Galeri.objects.get(pk=instance.pk)
                if old_instance.foto != instance.foto:
                    if old_instance.foto:
                        old_foto_path = old_instance.foto.path
                        if os.path.exists(old_foto_path) and old_foto_path != instance.foto.path:
                            os.remove(old_foto_path)
                    # Tidak perlu memeriksa foto baru, foto baru sudah disimpan saat update

    except ObjectDoesNotExist:
        print(f"User with username {user.username} does not exist.")

@receiver(post_delete, sender=Galeri)
def log_galeri_delete(sender, instance, **kwargs):
    user = instance.user
    aksi = f'Menghapus Galeri: {instance.url_link}'

    try:
        user_instance = User.objects.get(username=user.username)
        Aktivitas.objects.create(user=user_instance, aksi=aksi)

        # Hapus foto saat galeri dihapus
        if instance.foto:
            foto_path = instance.foto.path
            if os.path.exists(foto_path):
                os.remove(foto_path)
    except ObjectDoesNotExist:
        print(f"User with username {user.username} does not exist.")
