from django import template
from django import template
from Open_position.models import OpenPosition
from app.models import OrganizationMaster


register = template.Library()

@register.filter
def pluck(queryset, field_name):
    """Returns a list of the values of the specified field from a queryset."""
    return [getattr(item, field_name) for item in queryset]




@register.filter
def get_organization_name_by_location(location_number):
    try:
        # Find all positions with the given location number
        positions = OpenPosition.objects.filter(Locations=location_number)
        
        # If there are any positions, use the first one
        if positions.exists():
            position = positions.first()
            organization_id = position.Locations
            
            # Retrieve the organization name based on the OrganizationID
            organization = OrganizationMaster.objects.get(OrganizationID=organization_id)
            
            # Return the Organization Name
            return organization.ShortDisplayLabel
        
        return "Unknown Location"
    
    except OrganizationMaster.DoesNotExist:
        return "Unknown Organization"
    
@register.filter
def get_organization_name_by_locationfullnmee(location_number):
    try:
        # Find all positions with the given location number
        positions = OpenPosition.objects.filter(Locations=location_number)
        
        # If there are any positions, use the first one
        if positions.exists():
            position = positions.first()
            organization_id = position.Locations
            
            # Retrieve the organization name based on the OrganizationID
            organization = OrganizationMaster.objects.get(OrganizationID=organization_id)
            
            # Return the Organization Name
            return organization.OrganizationName
        
        return "Unknown Location"
    
    except OrganizationMaster.DoesNotExist:
        return "Unknown Organization"



@register.filter
def first_and_middle(value):
    """
    Returns everything except the last word (usually last name)
    Example: 'vasu dev pareek' → 'vasu dev'
    """
    if not value:
        return ''
    parts = value.strip().split()
    return ' '.join(parts[:-1]) if len(parts) > 1 else parts[0]
