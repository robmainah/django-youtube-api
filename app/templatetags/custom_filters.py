from django import template
from numerize import numerize

register = template.Library()

def format_numbers(value):
    return numerize.numerize(int(value))


register.filter('human_readable', format_numbers)
