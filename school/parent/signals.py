from django.dispatch import receiver
from useraccounts.models import MyUser
from django.dispatch import Signal
from parent.models import Parent

parent_signup_signal = Signal()


@receiver(parent_signup_signal)
def handle_parent_signup(sender, user, **kwargs):
    instance = Parent.objects.create(user=user).save()
