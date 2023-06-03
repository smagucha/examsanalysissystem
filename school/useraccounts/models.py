from django.db import models
from django.contrib.auth.models import Group

new_group, created = Group.objects.get_or_create(name="Admin")
new_group1, created = Group.objects.get_or_create(name="Teacher")
new_group2, created = Group.objects.get_or_create(name="Parent")
