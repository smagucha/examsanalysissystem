from django.dispatch import receiver
from useraccounts.models import MyUser
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from .models import Parent


# @receiver(post_save, sender=MyUser)
# def update_profile(sender, created, instance, **kwargs):
#     if created:
#         parent = Parent.objects.create(user=instance)
#         parent.save()
# #


@receiver(post_save, sender=MyUser)  # Update with the actual User model name
def assign_parent_group(sender, instance, created, **kwargs):
    if created and instance in MyUser.objects.filter(groups__name="Parent"):
        parent = Parent.objects.create(user=instance)
        parent.save()
        print(parent)


# @receiver(post_save, sender=MyUser)  # Update with the actual User model name
# def assign_teacher_group(sender, instance, created, **kwargs):
#     if created and instance.groups.filter(name="Teacher").exists():
#         # User belongs to the "Teacher" group
#         # Perform actions specific to the "Teacher" group
