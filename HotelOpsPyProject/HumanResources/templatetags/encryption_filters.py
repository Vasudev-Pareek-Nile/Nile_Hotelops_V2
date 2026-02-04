from django import template
from  hotelopsmgmtpy.utils import encrypt_id
from django import template
import locale
from HumanResources.models import EmployeePersonalDetails

register = template.Library()

@register.filter
def encrypt_id_filter(value):
    return encrypt_id(value)

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, 'None')





@register.filter
def break_words(value, word_limit=5):
    words = value.split()
    result = ''
    for i in range(0, len(words), word_limit):
        result += ' '.join(words[i:i+word_limit]) + '<br>'
    return result



#locale.setlocale(locale.LC_ALL, 'en_IN.UTF-8')
@register.filter(name='formatingdata')
def formatingdata(num):
    if num is None:
        return '0'
 
    try:
        num = float(num)
    except (TypeError, ValueError):
        return '0'
 
   
    formatted_num = locale.format_string('%.1f', num, grouping=True)
 
    return formatted_num

@register.filter
def get(dictionary, key):
    """Gets the value from a dictionary for a given key."""
    return dictionary.get(key)



@register.filter(name='get_emp_name')
def get_emp_name(emp_code, organization_id):
    try:
        ed = EmployeePersonalDetails.objects.filter(IsDelete=False, EmployeeCode=emp_code, OrganizationID=organization_id).first()
        return f"{ed.FirstName} {ed.LastName}"
    except:
        return "No employee found"

