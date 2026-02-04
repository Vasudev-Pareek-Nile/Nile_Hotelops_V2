from django import template

register = template.Library()

@register.filter
def format_ymd_to_dmy(value):
    """
    Converts a date string from 'YYYY-MM-DD' to 'DD-MM-YYYY'.
    Returns original value if format is unexpected.
    """
    if not value:
        return ''
    try:
        parts = value.split('-')
        if len(parts) == 3:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        else:
            return value
    except Exception:
        return value
