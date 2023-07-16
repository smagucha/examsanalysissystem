from django.db import models
from useraccounts.models import MyUser
from django.contrib.auth.models import User


class Parent(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": "Parent"},
        null=True,
        blank=True,
    )

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        verbose_name_plural = "parents"
