from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Closet


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Closet.objects.create(owner=instance, private=False, style="main_closet")
        Closet.objects.create(owner=instance, private=False, style="liked_fits")
