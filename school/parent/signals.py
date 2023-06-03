from django.db.models import signals
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .models import Parent
from teacher.models import Teacher


@receiver(signals.post_save, sender=User)
def create_parent(sender, instance, created, **kwargs):
    if instance.groups.filter(name="Parent"):
        Parent.objects.create(user=instance)
