from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from teacher.models import Teacher
from django.db.models import signals


@receiver(signals.post_save, sender=User)
def create_parent(sender, instance, created, **kwargs):
    if instance.groups.filter(name="Teacher"):
        Teacher.objects.create(user=instance)
