from django import template
from django.contrib.auth.models import Group
from student.models import Klass, Stream

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False
