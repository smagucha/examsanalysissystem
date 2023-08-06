from django.db import models
from django.contrib.auth.models import Group
from student.models import Klass, Stream
from useraccounts.models import MyUser
from django.conf import settings
from result.models import subject


class Designation(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Teacher(models.Model):
    Gender = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    user = models.ForeignKey(
        MyUser,
        limit_choices_to=({"groups__name": "Teacher"}),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_of_appointment = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=Gender, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, blank=True)


class Teachersubjects(models.Model):
    user = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    Subject = models.ForeignKey(subject, on_delete=models.CASCADE)
    Class = models.ForeignKey(Klass, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "teacher subjects"
