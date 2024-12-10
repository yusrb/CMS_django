from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from admin_cms.models import User, Aktivitas
from user_cms.models import Konten

@receiver(post_save, sender=Konten)
def log_konten_save(sender, instance, created, **kwargs):
    user = instance.user
    aksi = f'Menambahkan Konten: {instance.judul}' if created else f'Mengubah Konten: {instance.judul}'
    
    try:
        user_instance = User.objects.get(username=user.username)
        Aktivitas.objects.create(user=user_instance, aksi=aksi)
    except ObjectDoesNotExist:
        print(f"User with username {user.username} does not exist.")

@receiver(post_delete, sender=Konten)
def log_konten_delete(sender, instance, **kwargs):
    user = instance.user
    aksi = f'Menghapus Konten: {instance.judul}'
    
    try:
        user_instance = User.objects.get(username=user.username)
        Aktivitas.objects.create(user=user_instance, aksi=aksi)
    except ObjectDoesNotExist:
        print(f"User with username {user.username} does not exist.")

# @receiver(post_save, sender=User)
# def create_user_theme(sender, instance, created, **kwargs):
#     if created:
#         print(f"Creating theme for user: {instance.username}")
#         Theme.objects.get_or_create(user=instance)
