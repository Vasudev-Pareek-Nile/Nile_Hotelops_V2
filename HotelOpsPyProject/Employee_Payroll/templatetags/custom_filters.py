from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_day(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_status(dictionary, key):
    return dictionary.get(key, '')


@register.filter
def format_time(value):
    """
    Formats a time object to 'HH:MM:SS' format.
    """
    if hasattr(value, 'strftime'):  # If it's a time object
        return value.strftime('%H:%M:%S')
    elif isinstance(value, str) and '.' in value:  # If it's a string
        return value.split('.')[0]
    return value


@register.filter
def format_date_string(value):
    try:
        date_obj = datetime.strptime(value, "%d %B %Y")
        return date_obj.strftime("%d/%m/%Y")
    except Exception:
        return value  # return original if it fails

