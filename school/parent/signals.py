from django.db.models import signals
from django.dispatch import receiver
from useraccounts.models import MyUser
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from .models import Parent


@receiver(post_save, sender=MyUser)
def update_profile(sender, created, instance, **kwargs):
    if created:
        parent = Parent.objects.create(user=instance)
        parent.save()
