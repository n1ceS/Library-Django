from django import template
from django.utils import timezone, translation
register = template.Library()


@register.filter(name='calculate_days')
def calculate_days(value):
    translation.activate('pl')
    return str(value - timezone.now()).split(" ")[0]