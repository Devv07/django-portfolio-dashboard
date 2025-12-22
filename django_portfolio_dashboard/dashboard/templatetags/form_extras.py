from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def attr(field, attr_str):
    key, value = attr_str.split(':')
    attrs = field.as_widget(attrs={key.strip(): value.strip()})
    return mark_safe(attrs)