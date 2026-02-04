    # custom_filters.py

from django import template

register = template.Library()

@register.filter(name='to_roman')
def to_roman(value):
    roman_numerals = {
        1: 'I',
        4: 'IV',
        5: 'V',
        9: 'IX',
        10: 'X',
        40: 'XL',
        50: 'L'
    }
    result = ''
    for numeral in sorted(roman_numerals.keys(), reverse=True):
        while value >= numeral:
            result += roman_numerals[numeral]
            value -= numeral
    return result
from datetime import datetime

@register.filter
def format_time(value):
    """
    Formats a time object to 'HH:M2M:SS' format.
    """
    if isinstance(value, datetime):
        if hasattr(value, 'strftime'):  # If it's a time object
            return value.strftime('%H:%M:%S')
        elif isinstance(value, str) and '.' in value:  # If it's a string
            return value.split('.')[0]
    return value