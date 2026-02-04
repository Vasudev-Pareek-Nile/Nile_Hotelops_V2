from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 'None')



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