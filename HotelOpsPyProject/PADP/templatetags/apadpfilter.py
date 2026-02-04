from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
import datetime
@register.filter
def getMonthHeader(MonthHeader):
    try:
        year, month = MonthHeader.split()
        monthlist=["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        # Step 2: Convert the month number to the month name
        month_name = monthlist[int(month)]

        # Step 3: Format the output
        formatted_date = f"{month_name} {year}"
        return formatted_date
    except:
        return MonthHeader





@register.filter
def format_time(value):
    # Split the string based on the underscore
    parts = value.split('_')
    
    # Handle case where the input is in the format '1_weeks' or '1_month'
    if len(parts) == 2:
        number, unit = parts
        # Capitalize the first letter of the unit and return the formatted string
        unit = unit.capitalize()
        return f"{number} {unit}"
    
    return value



import re
from django import template
from django.utils.safestring import mark_safe

# register = template.Library()
@register.filter(name='bold_lines_before_hyphen')
def bold_lines_before_hyphen(value):
    lines = value.split('\n')
    result_blocks = []

    for line in lines:
        if not line.strip():
            continue

        match = re.match(r'^(.*?)(\s*-\s*)(.*)', line.strip())
        if match:
            heading = match.group(1).strip()
            description = match.group(3).strip()

            html_block = f"""
                <div style='margin-bottom: 12px; line-height: 1.4;'>
                    <div style='font-weight: bold; color: cornflowerblue;'>{heading}</div>
                    <div>{description}</div>
                </div>
            """
            result_blocks.append(html_block)
        else:
            result_blocks.append(f"<div>{line.strip()}</div>")

    return mark_safe(''.join(result_blocks))