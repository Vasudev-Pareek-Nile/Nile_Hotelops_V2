from django import template

register = template.Library()

@register.filter
def add_amount(value, amount):
    return value + amount
