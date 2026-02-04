from django import template

register = template.Library()

@register.filter
def get_day(dictionary, key):
    return dictionary.get(key, '')



@register.filter
def get_MRI_day(dictionary, key):
    return dictionary.get(key, '')

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
def get_MRI_day_index(value, index):
    print(index)
    # Split the index parameter to get 'day' and 'index' separately
    try:
        day, idx = index.split(',')
        day = int(day)  # Convert to integer if needed
        idx = int(idx)  # Convert index to integer
        
        # Now, safely get the value from the row using the 'day' and 'index'
        # Assuming 'row' is a dictionary-like object where you can access values
        if isinstance(value, dict) and str(day) in value:
            # Get the MRI value at the index (you can customize this part)
            day_value = value.get(str(day), '')
            # Split the day value (which should have line breaks) and get the index element
            day_parts = day_value.split("^")
            if idx < len(day_parts):
                return day_parts[idx]  # Return the part at the given index
            return ""  # Return empty if the index is out of range
        return ""
    except Exception as e:
        return f""




@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
