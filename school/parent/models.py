from django.db import models
from django.contrib.auth.models import User


class Parent(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"groups__name": "Parent"},
        null=True,
        blank=True,
    )
    Idno = models.CharField(max_length=10, blank=True)
    phonenumber = models.CharField(max_length=13, blank=True)
    physical_add = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        verbose_name_plural = "parents"
