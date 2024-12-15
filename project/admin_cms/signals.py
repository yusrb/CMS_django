from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from admin_cms.models import Komunitas
from user_cms.models import Pertanyaan

@receiver(post_save, sender=Pertanyaan)
def update_pertanyaan_count_on_save(sender, instance, **kwargs):
    if instance.komunitas:
        instance.komunitas.update_pertanyaan_count()

@receiver(post_delete, sender=Pertanyaan)
def update_pertanyaan_count_on_delete(sender, instance, **kwargs):
    if instance.komunitas:
        instance.komunitas.update_pertanyaan_count()
