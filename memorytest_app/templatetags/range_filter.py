# memorytest_app/templatetags/range_filter.py
from django import template

register = template.Library()

@register.filter
def range_filter(value):
    return range(value)
