from django import template

register = template.Library()


@register.filter(name='get_value')
def get_value(obj, field_name):
    return getattr(obj, field_name, None)