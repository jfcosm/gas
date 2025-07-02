from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import DistribuidorUsuario

@receiver(post_save, sender=User)
def crear_perfil_distribuidor(sender, instance, created, **kwargs):
    if created:
        DistribuidorUsuario.objects.create(user=instance)
