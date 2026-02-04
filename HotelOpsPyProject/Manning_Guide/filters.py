def apply_filters(queryset, filter_criteria):
    """
    Apply filters to a queryset based on given criteria.

    Args:
    - queryset: The initial queryset to filter.
    - filter_criteria: List of dictionaries containing filter criteria.

    Returns:
    - Filtered queryset.
    """
    for criterion in filter_criteria:
         field = criterion.get('field', {}).get('value')
         operator = criterion.get('operator', {}).get('value')
         value = criterion.get('value', {}).get('value')

         if not field or not operator or value is None:
             continue

         filter_kwargs = {}
         print(f"Applying filter: Field={field}, Operator={operator}, Value={value}")

         if operator == 'eq':
             filter_kwargs[f"{field}"] = value
         elif operator == 'ne':
             queryset = queryset.exclude(**{f"{field}": value})
         elif operator == 'sw':
             filter_kwargs[f"{field}__startswith"] = value
         elif operator == 'ct':
             filter_kwargs[f"{field}__icontains"] = value
         elif operator == 'nct':
             queryset = queryset.exclude(**{f"{field}__icontains": value})
         elif operator == 'fw':
             filter_kwargs[f"{field}__endswith"] = value
         elif operator == 'in':
             filter_kwargs[f"{field}__in"] = value.split(',')
         elif operator == 'null':
             filter_kwargs[f"{field}__isnull"] = True
         elif operator == 'nn':
             filter_kwargs[f"{field}__isnull"] = False
         elif operator == 'gt':
             filter_kwargs[f"{field}__gt"] = value
         elif operator == 'lt':
             filter_kwargs[f"{field}__lt"] = value
         elif operator == 'bw':
             range_values = value.split(',')
             if len(range_values) == 2:
                 filter_kwargs[f"{field}__range"] = (range_values[0], range_values[1])
         elif operator == 'nbw':
             range_values = value.split(',')
             if len(range_values) == 2:
                 queryset = queryset.exclude(**{f"{field}__range": (range_values[0], range_values[1])})
         elif operator == 'bool':
             filter_kwargs[f"{field}"] = value.lower() == 'true'

         print(f"Filter kwargs: {filter_kwargs}")
         queryset = queryset.filter(**filter_kwargs)

    return queryset
# from django.db.models import F, Value
# from django.db.models.functions import Coalesce

# def apply_filters(queryset, filter_criteria):
#     """
#     Apply filters to a queryset based on given criteria.

#     Args:
#     - queryset: The initial queryset to filter.
#     - filter_criteria: List of dictionaries containing filter criteria.

#     Returns:
#     - Filtered queryset.
#     """
#     for criterion in filter_criteria:
#         field = criterion.get('field', {}).get('value')
#         operator = criterion.get('operator', {}).get('value')
#         value = criterion.get('value', {}).get('value')
#         if field == 'Lavel':
#             if operator == 'eq':
#                     queryset = queryset.filter(
#                         **{f'on_roll_designation_master__Lavel': Value(value, output_field=CharField())}
#                     )
#             elif operator == 'in':
#                     queryset = queryset.filter(
#                         on_roll_designation_master__Lavel__in=value
#                     )
#             else:
#                     raise ValueError(f"Unsupported operator '{operator}' for field '{field}'")
            
#         if not field or not operator or value is None:
#             continue

#         filter_kwargs = {}
#         print(f"Applying filter: Field={field}, Operator={operator}, Value={value}")

       
        

       

#         try:
#             if operator == 'eq':
#                 filter_kwargs[f"{annotated_field}"] = value
#             elif operator == 'ne':
#                 queryset = queryset.exclude(**{f"{annotated_field}": value})
#             elif operator == 'sw':
#                 filter_kwargs[f"{annotated_field}__startswith"] = value
#             elif operator == 'ct':
#                 filter_kwargs[f"{annotated_field}__icontains"] = value
#             elif operator == 'nct':
#                 queryset = queryset.exclude(**{f"{annotated_field}__icontains": value})
#             elif operator == 'fw':
#                 filter_kwargs[f"{annotated_field}__endswith"] = value
#             elif operator == 'in':
#                 filter_kwargs[f"{annotated_field}__in"] = value.split(',')
#             elif operator == 'null':
#                 filter_kwargs[f"{annotated_field}"] = 0
#             elif operator == 'nn':
#                 queryset = queryset.exclude(**{f"{annotated_field}": 0})
#             elif operator == 'gt':
#                 filter_kwargs[f"{annotated_field}__gt"] = value
#             elif operator == 'lt':
#                 filter_kwargs[f"{annotated_field}__lt"] = value
#             elif operator == 'bw':
#                 range_values = value.split(',')
#                 if len(range_values) == 2:
#                     filter_kwargs[f"{annotated_field}__range"] = (range_values[0], range_values[1])
#             elif operator == 'nbw':
#                 range_values = value.split(',')
#                 if len(range_values) == 2:
#                     queryset = queryset.exclude(**{f"{annotated_field}__range": (range_values[0], range_values[1])})
#             elif operator == 'bool':
#                 filter_kwargs[f"{annotated_field}"] = value.lower() == 'true'

#             print(f"Filter kwargs: {filter_kwargs}")
#             queryset = queryset.filter(**filter_kwargs)
#         except Exception as e:
#             print(f"Error applying filter: {e}")
#             raise

#     return queryset
