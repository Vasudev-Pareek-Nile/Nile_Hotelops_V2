from django import template
import locale
register = template.Library()




register = template.Library()

# @register.filter(name='formatingdata')
# def formatingdata(num):
#     if num is None:
#         return '0'

#     try:
#         num = int(float(num))  # Convert to float then int to remove decimal part
#     except (TypeError, ValueError):
#         return '0'

#     integer_part = str(num)
#     reversed_digits = list(reversed(integer_part))

#     grouped = []
#     for i, digit in enumerate(reversed_digits):
#         if i == 3 or (i > 3 and (i - 1) % 2 == 0):
#             grouped.append(',')
#         grouped.append(digit)

#     formatted_int = ''.join(reversed(grouped))
#     return formatted_int


@register.filter(name='formatingdata')
def formatingdata(num):
    if num is None:
        return '0'

    try:
        num = int(float(num))  # Convert to float then int to remove decimal part
    except (TypeError, ValueError):
        return '0'

    sign = "-" if num < 0 else ""   # capture the negative sign
    integer_part = str(abs(num))    # work only with the absolute value

    reversed_digits = list(reversed(integer_part))
    grouped = []

    for i, digit in enumerate(reversed_digits):
        if i == 3 or (i > 3 and (i - 1) % 2 == 0):
            grouped.append(',')
        grouped.append(digit)

    formatted_int = ''.join(reversed(grouped))
    return sign + formatted_int     # add the sign back


# @register.filter(name='formatingCommaData')
# def formatingCommaData(num):
#     if num is None:
#         return '0'

#     try:
#         num = float(num)
#     except (TypeError, ValueError):
#         return '0'

#     # Split integer and decimal parts
#     num_parts = str(f'{num:.1f}').split('.')
#     integer_part = num_parts[0]
#     decimal_part = num_parts[1]

#     # Reverse the integer part for easier processing
#     reversed_digits = list(reversed(integer_part))

#     # Format Indian-style (first group of 3, then every 2 digits)
#     grouped = []
#     for i, digit in enumerate(reversed_digits):
#         if i == 3 or (i > 3 and (i - 1) % 2 == 0):
#             grouped.append(',')
#         grouped.append(digit)

#     formatted_int = ''.join(reversed(grouped))
#     return f"{formatted_int}.{decimal_part}"


# @register.filter(name='formatingdata')
# def formatingdata(num):
#     if num is None:
#         return '0'

#     try:
#         num = float(num)
#     except (TypeError, ValueError):
#         return '0'

    
#     formatted_num = locale.format_string('%.1f', num, grouping=True)

#     return formatted_num

@register.filter(name='get_item')
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None  

@register.filter(name='get')
def get(dictionary, key):
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None  

@register.filter
def nested_get(dictionary, keys):
    """Retrieve a value from a nested dictionary using a comma-separated string of keys."""
    if not isinstance(dictionary, dict):
        return None

    key_list = keys.split(',') if isinstance(keys, str) else keys
    value = dictionary
    for key in key_list:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None
    return value
    
@register.filter(name='dict_key')
def dict_key(dictionary, key):
    """
    Returns the value for a given key from a dictionary.
    """
    return dictionary.get(key, {})    











@register.filter
def variance_color(value):
    try:
        value = float(value)
        return 'green' if value < 0 else 'red'
    except (ValueError, TypeError):
        return 'black'  # Default color in case of an error
    

@register.filter
def join_key(division, department):
    """Join division and department with double underscore for template lookup"""
    return f"{division}__{department}"



# To convert Number with commma
# @register.filter
# def indian_currency(value):
#     try:
#         value = float(value)
#         s = str(int(value))
#         if len(s) <= 3:
#             result = s
#         else:
#             # Start from right, take last 3 digits
#             result = s[-3:]
#             s = s[:-3]
#             # Add commas after every 2 digits
#             while len(s) > 0:
#                 result = s[-2:] + ',' + result
#                 s = s[:-2]
#         # Add decimal part
#         decimal_part = f"{value:.2f}".split('.')[1]
#         return result + '.' + decimal_part
#     except:
#         return value
    
@register.filter
def indian_currency(value):
    try:
        value = float(value)
        is_negative = value < 0
        value = abs(value)  # work with positive part only
        
        s = str(int(value))
        if len(s) <= 3:
            result = s
        else:
            result = s[-3:]
            s = s[:-3]
            while len(s) > 0:
                result = s[-2:] + ',' + result
                s = s[:-2]

        decimal_part = f"{value:.2f}".split('.')[1]
        formatted = result + '.' + decimal_part
        
        return f"-{formatted}" if is_negative else formatted
    except:
        return value
