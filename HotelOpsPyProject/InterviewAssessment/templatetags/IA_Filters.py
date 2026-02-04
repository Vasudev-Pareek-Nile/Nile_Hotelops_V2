from django import template

register = template.Library()

@register.filter(name='indian_currency')
def indian_currency(value):
    try:
        value = float(value)  
        value = int(value)  
        return "₹{:,}".format(value).replace(',', 'X').replace('.', ',').replace('X', ',')
    except (ValueError, TypeError):
        return value  
