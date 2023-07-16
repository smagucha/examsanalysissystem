from django.dispatch import receiver
from useraccounts.models import MyUser
from django.dispatch import Signal
from .models import Teacher

teacher_signup_signal = Signal()


@receiver(teacher_signup_signal)
def handle_teacher_signup(sender, user, **kwargs):
    instance = Teacher.objects.create(user=user).save()
