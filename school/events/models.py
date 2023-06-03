from django.db import models

from django.db import models
from datetime import date


class SchoolEvents(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    dateevents = models.DateField()
    year = models.CharField(
        max_length=4, default=date.today().year, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "school events"

    def __str__(self):
        return self.name
