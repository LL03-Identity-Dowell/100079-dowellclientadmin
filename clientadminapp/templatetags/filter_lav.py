from django import template
register = template.Library()
@register.filter()
def low(value):
    return value.lower()
@register.filter(name='zip')
def zip_lists(a, b):
  return zip(a, b)