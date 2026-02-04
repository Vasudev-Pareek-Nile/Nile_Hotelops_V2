from django import template
import calendar

register = template.Library()

@register.filter
def month_name(month_number):
    try:
        return calendar.month_abbr[int(month_number)]
    except (ValueError, IndexError):
        return month_number  # fallback if invalid

@register.filter
def pad_month(value):
    """Ensure the month is always two digits."""
    try:
        return f"{int(value):02d}"
    except:
        return value
    

# myapp/templatetags/custom_filters.py

# from django import template

# register = template.Library()

@register.filter
def truncate_decimal(value):
    try:
        return str(value).split('.')[0]
    except:
        return value
