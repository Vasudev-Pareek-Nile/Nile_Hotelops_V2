from django.shortcuts import render,get_object_or_404,redirect
from .models import upload_data,FileUpload,PartnerRating
from django.utils import timezone
import pandas as pd
from django.http import HttpResponse
from .forms import UploadFileForm
from datetime import datetime 
from app.models import OrganizationMaster
from django.db.models import Avg, Count
from app.models import OrganizationMaster
import re
from collections import defaultdict
from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from textblob import TextBlob
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponseForbidden
from hotelopsmgmtpy.GlobalConfig import MasterAttribute    
import numpy as np   
from django.db.models import Q


def handle_uploaded_file(f,OrganizationID,software):
    if software=="reviewPro":
        df = pd.read_excel(f, engine='openpyxl',skiprows=7)
        required_columns = [
        'Reviewer',
        'Review Rating',
        'SERVICE', 
        'ROOM', 
        'VALUE', 
        'CLEANLINESS', 
        'Classification',
        'LOCATION', 
        'Review Text', 
        'Review Title', 
        'Management Response', 
        'Reply Date', 
        'Source'
        ]
    
        df_filtered = df[required_columns]
        data = df_filtered.to_dict(orient='records')
        # try:
        for row in data:
            hotel_rating = clean_float_value(row.get('Review Rating') or 0)
            reviewer = clean_float_value(row.get('Reviewer') or 0)
            service = clean_float_value(row.get('SERVICE') or 0)
            room = clean_float_value(row.get('ROOM') or 0)
            value = clean_float_value(row.get('VALUE') or 0)
            cleanliness = clean_float_value(row.get('CLEANLINESS') or 0)
            classification = row.get('Classification')
            location = clean_float_value(row.get('LOCATION'))
            review_text = row.get('Review Text')
            review_title = row.get('Review Title')
            management_response = row.get('Management Response')
            reply_date = None
            try:
                #reply_date = pd.to_datetime(row.get('Reply Date'), dayfirst=True, errors='coerce')
                reply_date = pd.to_datetime(row.get['Reply Date'], format='%d/%m/%Y', errors='coerce')
            except Exception as e:
                print(f"Error parsing reply_date: {e}")
                
            
            source = row.get('Source')

            def safe_float_conversion(value):
                try:
                    return float(value)
                except (TypeError, ValueError):
                    return None

            # service = clean_float_value(service)
            # room = clean_float_value(room)
            # value = clean_float_value(value)
            # cleanliness = clean_float_value(cleanliness)

            # Create object
            upload_data.objects.create(
                hotel=hotel_rating,  
                reviewer=reviewer,
                service=service,
                room=room,
                value=value,
                cleanliness=cleanliness,
                classification=classification,
                location=location,
                review_text=review_text,
                review_title=review_title,
                management_response=management_response,
                reply_date=reply_date,
                source=source,
                OrganizationID=OrganizationID,
            )
        # except Exception as e:
        #     print(f"Error in creating view: {e}")  # Log the exception


    else:
        df = pd.read_excel(f, engine='openpyxl', header=0)
        required_columns = [
        'Reviewer Name',
        'Rating', 
        'Sentiment',
        'Review Text', 
        'Review Title', 
        'Review Reply', 
        'Read At', 
        'Platform'
        ]
        df_filtered = df[required_columns]
        data = df_filtered.to_dict(orient='records')
        for row in data:
            upload_data.objects.create(
            hotel= row.get('Rating'),
            reviwer=row.get('Reviewer Name'),
            classification=row.get('Sentiment'),
            review_text=row.get('Review Text'),
            review_title=row.get('Review Title'),
            management_response=row.get('Review Reply'),
            reply_date=pd.to_datetime(row.get('Read At'), errors='coerce').date() if pd.notna(row.get('Read At')) else None,
            source=row.get('Platform'),
            OrganizationID=OrganizationID,   
        )
    
def upload_file(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]
    print("dj",OrganizationID)
    if OrganizationID == "3":
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
    else:
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID)

    organization_choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in organizations]

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES.get('file')
            second_file = request.FILES.get('second_file')
            date = form.cleaned_data['date']
            OrganizationID = form.cleaned_data['OrganizationID']
            print("ak",OrganizationID)

            Organization = get_object_or_404(OrganizationMaster, OrganizationID=OrganizationID)

            if Organization.ReviewSoftware == "reviewPro":
                if file:
                    handle_uploaded_file(file, OrganizationID,Organization.ReviewSoftware)
                else:
                    form.add_error('file', 'Primary file is required for reviewPro organizations.')
            elif Organization.ReviewSoftware == "Rankly":
                if file:
                    handle_uploaded_file(file, OrganizationID,Organization.ReviewSoftware)
                else:
                    form.add_error('file', 'Primary file is required for Rankly organizations.')

            else:    
                if file and second_file:
                    excelFileData(file, OrganizationID, second_file)
                else:
                    form.add_error(None, "Both files are required for non-reviewPro organizations.")

        
            averages, review_list, classification_dict, source_dict, data, total_dict = dataShow(OrganizationID)
            if OrganizationID == "3":
                organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
            else:
                organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID)
                
            organization_choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in organizations]
            
            return render(request, 'review/display_data.html', {
                'averages': averages,
                'reviewslist': review_list,
                "classification_counts": classification_dict,
                "source_counts": source_dict,
                'organization_choices': organization_choices,
                'data': data,
                'total_dict': total_dict
            })
    else:
        form = UploadFileForm()
    return render(request, 'review/upload.html', {'form': form, 'organization_choices': organization_choices})


def show_data(request):
    if 'OrganizationID' not in request.session:
        return redirect(MasterAttribute.Host)
    else:
        OrganizationID = request.session["OrganizationID"]
    averages ,review_list,classification_dict,source_dict,data,total_dict=dataShow(OrganizationID)
    if OrganizationID == "3":
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
    else:
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID)
    organization_choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in organizations]

    return render(request, 'review/display_data.html', {'averages': averages ,'reviewslist': review_list,"classification_counts":classification_dict,"source_counts":source_dict,'organization_choices': organization_choices,'data':data,'total_dict':total_dict})
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404
from collections import defaultdict
# from .models import OrganizationMaster, upload_data, PartnerRating
from django.db import models


def dataShow(OrganizationID=None):
    if OrganizationID==None:
        print("Hello")
        
            # Get the averages for the relevant fields, filtering out NULL values
        averages = upload_data.objects.aggregate(
            avg_service=Avg('service', filter=models.Q(service__isnull=False)),
            avg_room=Avg('room', filter=models.Q(room__isnull=False)),
            avg_value=Avg('value', filter=models.Q(value__isnull=False)),
            avg_cleanliness=Avg('cleanliness', filter=models.Q(cleanliness__isnull=False)),
            avg_location=Avg('location', filter=models.Q(location__isnull=False)),
            avg_hotel=Avg('hotel', filter=models.Q(hotel__isnull=False))
        )
        
        # Round the averages only if they are not None
        averages = {key: round(value, 1) if value is not None else None for key, value in averages.items()}

        # Partner Ratings
        partner_data = PartnerRating.objects.all()
        data = {}
        for rating in partner_data:
            if rating.partner_type == 'MakeMyTrip':
                data[rating.partner_type] = {
                    'Overall_Rating': rating.overall_rating,
                    'Service': rating.service * 2,
                    'Facilities': rating.facilities * 2,
                    'Cleanliness': rating.cleanliness * 2,
                    'Room': rating.room,
                    'Value': rating.value * 2,
                    'Location': rating.location * 2,
                    'Food': rating.food * 2,
                    'Wifi': rating.wifi * 2
                }
            else:
                data[rating.partner_type] = {
                    'Overall_Rating': rating.overall_rating / 2,
                    'Service': rating.service,
                    'Facilities': rating.facilities,
                    'Cleanliness': rating.cleanliness,
                    'Room': rating.room,
                    'Value': rating.value,
                    'Location': rating.location,
                    'Food': rating.food,
                    'Wifi': rating.wifi
                }

        # Classification counts
        classification_counts = upload_data.objects.all().values('classification').annotate(
            count=Count('classification')
        )
        classification_dict = {item['classification']: item['count'] for item in classification_counts}

        # Source counts
        source_counts = upload_data.objects.all().values('source').annotate(
            count=Count('source')
        )
        source_dict = {item['source']: item['count'] for item in source_counts}

        # Review data
        review_list = upload_data.objects.all().order_by('-reply_date')
        total_response = upload_data.objects.filter( management_response__isnull=False).count()
        total_count = upload_data.objects.all().count()

        total_dict = {
            "total_review": total_count,
            "total_response": total_response
        }

        return averages, review_list, classification_dict, source_dict, data, total_dict

    else:
    # Fetch the organization
        Organization = get_object_or_404(OrganizationMaster, OrganizationID=OrganizationID)
        
        if Organization.ReviewSoftware == "reviewPro":
            # Get the averages for the relevant fields, filtering out NULL values
            averages = upload_data.objects.filter(OrganizationID=OrganizationID).aggregate(
                avg_service=Avg('service', filter=models.Q(service__isnull=False)),
                avg_room=Avg('room', filter=models.Q(room__isnull=False)),
                avg_value=Avg('value', filter=models.Q(value__isnull=False)),
                avg_cleanliness=Avg('cleanliness', filter=models.Q(cleanliness__isnull=False)),
                avg_location=Avg('location', filter=models.Q(location__isnull=False)),
                avg_hotel=Avg('hotel', filter=models.Q(hotel__isnull=False))
            )
            
            # Round the averages only if they are not None
            averages = {key: round(value, 1) if value is not None else None for key, value in averages.items()}

            # Partner Ratings
            partner_data = PartnerRating.objects.filter(OrganizationID=OrganizationID)
            data = {}
            for rating in partner_data:
                if rating.partner_type == 'MakeMyTrip':
                    data[rating.partner_type] = {
                        'Overall_Rating': rating.overall_rating,
                        'Service': rating.service * 2,
                        'Facilities': rating.facilities * 2,
                        'Cleanliness': rating.cleanliness * 2,
                        'Room': rating.room,
                        'Value': rating.value * 2,
                        'Location': rating.location * 2,
                        'Food': rating.food * 2,
                        'Wifi': rating.wifi * 2
                    }
                else:
                    data[rating.partner_type] = {
                        'Overall_Rating': rating.overall_rating / 2,
                        'Service': rating.service,
                        'Facilities': rating.facilities,
                        'Cleanliness': rating.cleanliness,
                        'Room': rating.room,
                        'Value': rating.value,
                        'Location': rating.location,
                        'Food': rating.food,
                        'Wifi': rating.wifi
                    }

            # Classification counts
            classification_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('classification').annotate(
                count=Count('classification')
            )
            classification_dict = {item['classification']: item['count'] for item in classification_counts}

            # Source counts
            source_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('source').annotate(
                count=Count('source')
            )
            source_dict = {item['source']: item['count'] for item in source_counts}

            # Review data
            review_list = upload_data.objects.filter(OrganizationID=OrganizationID).order_by('-reply_date')
            total_response = upload_data.objects.filter(OrganizationID=OrganizationID, management_response__isnull=False).count()
            total_count = upload_data.objects.filter(OrganizationID=OrganizationID).count()

            total_dict = {
                "total_review": total_count,
                "total_response": total_response
            }

            return averages, review_list, classification_dict, source_dict, data, total_dict

        else:
            # For non-reviewPro, calculate averages differently
            averages = upload_data.objects.filter(OrganizationID=OrganizationID).aggregate(
                avg_hotel=Avg('hotel'),
                avg_service=Avg('service'),
                avg_room=Avg('room'),
                avg_value=Avg('value'),
                avg_cleanliness=Avg('cleanliness')
            )
            averages = {key: round(value / 2, 1) if value is not None else None for key, value in averages.items()}

            # Classification counts with mapping
            classification_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('classification').annotate(
                count=Count('classification')
            )
            classification_dict = {item['classification']: item['count'] for item in classification_counts}

            classification_mapping = {
                'Detractors': 'Negative',
                'Detractors - Negative': 'Negative',
                'Passives': 'Neutral',
                'Promoters': 'Positive',
                'Promoters - Positive': 'Positive',
            }
            
            # Aggregate classification counts
            aggregated_counts = defaultdict(int)
            for classification, count in classification_dict.items():
                category = classification_mapping.get(classification, 'Unknown')
                aggregated_counts[category] += count
            aggregated_counts = dict(aggregated_counts)

            # Source counts with mapping
            source_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('source').annotate(
                count=Count('source')
            )
            source_dict = {item['source']: item['count'] for item in source_counts}

            source_mapping = {
                'AGODA': 'Agoda',
                'BOOKING': 'Booking.com',
                'GOOGLE_LOCAL': 'Google',
                'MAKE_MY_TRIP': 'MakeMyTrip',
                'TRIPADVISOR': 'Tripadvisor',
            }
            
            # Aggregate source counts
            aggregated_source_counts = defaultdict(int)
            for source, count in source_dict.items():
                source_type = source_mapping.get(source, 'Unknown')
                aggregated_source_counts[source_type] += count
            aggregated_source_counts = dict(aggregated_source_counts)

            # Partner Ratings
            partner_data = PartnerRating.objects.filter(OrganizationID=OrganizationID)
            data = {}
            for rating in partner_data:
                if rating.partner_type == 'MakeMyTrip':
                    data[rating.partner_type] = {
                        'Overall_Rating': rating.overall_rating,
                        'Service': rating.service * 2,
                        'Facilities': rating.facilities * 2,
                        'Cleanliness': rating.cleanliness * 2,
                        'Room': rating.room,
                        'Value': rating.value * 2,
                        'Location': rating.location * 2,
                        'Food': rating.food * 2,
                        'Wifi': rating.wifi * 2
                    }
                else:
                    data[rating.partner_type] = {
                        'Overall_Rating': rating.overall_rating / 2,
                        'Service': rating.service,
                        'Facilities': rating.facilities,
                        'Cleanliness': rating.cleanliness,
                        'Room': rating.room,
                        'Value': rating.value,
                        'Location': rating.location,
                        'Food': rating.food,
                        'Wifi': rating.wifi
                    }

            # Review data
            review_list = upload_data.objects.filter(OrganizationID=OrganizationID).order_by('-reply_date')
            total_response = upload_data.objects.filter(OrganizationID=OrganizationID, management_response__isnull=False).count()
            total_count = upload_data.objects.filter(OrganizationID=OrganizationID).count()

            total_dict = {
                "total_review": total_count,
                "total_response": total_response
            }

            return averages, review_list, aggregated_counts, aggregated_source_counts, data, total_dict

def dataShowold(OrganizationID):
    if OrganizationID:
        Organization= get_object_or_404(OrganizationMaster, OrganizationID=OrganizationID)
        review_software= Organization.ReviewSoftware 
        if review_software=="reviewPro":
            averages = upload_data.objects.filter(OrganizationID=OrganizationID).aggregate(
                avg_service=Avg('service'),
                avg_room=Avg('room'),
                avg_value=Avg('value'),
                avg_cleanliness=Avg('cleanliness'),
                avg_location=Avg('location'),
                avg_hotel=Avg('hotel')
            )
            averages = {key: round(value, 1) for key, value in averages.items() if value is not None}
        elif review_software=="reviewPro":
            averages = upload_data.objects.filter(OrganizationID=OrganizationID).aggregate(
            avg_hotel=Avg('hotel'),
            avg_service=Avg('service'),
            avg_room=Avg('room'),
            avg_value=Avg('value'),
            avg_cleanliness=Avg('cleanliness'),
            )
            averages = {key: round(value, 1) for key, value in averages.items() if value is not None}
        else:
            averages={}

        source_list=['Google','Tripadvisor','Agoda','MakeMyTrip']
        source_list_results = {}

        for source in source_list:
            aggregation = upload_data.objects.filter(
                OrganizationID=OrganizationID,
                source=source
            ).aggregate(
                Service=Avg('service'),
                Room=Avg('room'),
                Value=Avg('value'),
                Cleanliness=Avg('cleanliness'),
                Location=Avg('location')
                )
            source_dict = {key: round(value, 1) for key, value in aggregation.items() if value is not None}
            source_list_results[source] = source_dict
            
        partner_data=PartnerRating.objects.filter(OrganizationID=OrganizationID).order_by('CreatedBy')
        data = {}
        for rating in partner_data:
            if rating.partner_type == 'MakeMyTrip':
                data[rating.partner_type] = {
                    'Overall_Rating': rating.overall_rating,
                    'Service': rating.service * 2,
                    'Facilities': rating.facilities * 2,
                    'Cleanliness': rating.cleanliness * 2,
                    'Room': rating.room,
                    'Value': rating.value * 2,
                    'Location': rating.location * 2,
                    'Food': rating.food * 2,
                    'Wifi': rating.wifi * 2
                    }
            else:
                data[rating.partner_type] = {
                    'Overall_Rating': rating.overall_rating/2,
                    'Service': rating.service,
                    'Facilities': rating.facilities,
                    'Cleanliness': rating.cleanliness,
                    'Room': rating.room,
                    'Value': rating.value,
                    'Location': rating.location,
                    'Food': rating.food,
                    'Wifi': rating.wifi
                    }
        
        
        data = data if data else source_list_results
        classification_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('classification').annotate(
            count=Count('classification')
            )
            
        classification_dict = {item['classification']: item['count'] for item in classification_counts}
        source_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('source').annotate(
            count=Count('source')
            )
        source_dict = {item['source']: item['count'] for item in source_counts}
            
            
        review_list = upload_data.objects.filter(OrganizationID=OrganizationID).order_by('-reply_date')
        total_response = upload_data.objects.filter(OrganizationID=OrganizationID, management_response__isnull=False).count()
        total_count = upload_data.objects.filter(OrganizationID=OrganizationID).count()
        total_dict = {
            "total_review":total_count,
            "total_response":total_response

        }
            
        return averages ,review_list,classification_dict,source_dict,data,total_dict
    else:
        cumulative_classification_counts = defaultdict(int)
        source_count_dict=defaultdict(int)
        organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
        total_averages = {
            'avg_service': 0,
            'avg_room': 0,
            'avg_value': 0,
            'avg_cleanliness': 0,
            'avg_location': 0,
            'avg_hotel': 0,
        }
        total_counts = {
            'review_count': 0,
            'response_count': 0,
        }

        source_list_results = {}
        partner_data = {}
        count_average=0
        all_reviews = []
        overall_averages = defaultdict(list)

        for org in organizations:
            OrganizationID=org.OrganizationID
           
            averages = upload_data.objects.filter(OrganizationID=OrganizationID).aggregate(
                avg_service=Avg('service', filter=Q(service__isnull=False)),
                avg_room=Avg('room', filter=Q(room__isnull=False)),
                avg_value=Avg('value', filter=Q(value__isnull=False)),
                avg_cleanliness=Avg('cleanliness', filter=Q(cleanliness__isnull=False)),
                avg_location=Avg('location', filter=Q(location__isnull=False)),
                avg_hotel=Avg('hotel', filter=Q(hotel__isnull=False))
            )

            # for key in total_averages.keys():
            #     if averages.get(key):
            #         count_average += 1
            #         total_averages[key] += averages.get(key, 0) or 0
            for key, value in averages.items():
                if value is not None: 
                    overall_averages[key].append(value)

            partner_ratings = PartnerRating.objects.filter(OrganizationID=OrganizationID)
            for rating in partner_ratings:
                if rating.partner_type not in partner_data:
                    partner_data[rating.partner_type] = {
                        'Overall_Rating': 0,
                        'Service': 0,
                        'Facilities': 0,
                        'Cleanliness': 0,
                        'Room': 0,
                        'Value': 0,
                        'Location': 0,
                        'Food': 0,
                        'Wifi': 0,
                        'count': 0
                    }
                partner_data[rating.partner_type]['Overall_Rating'] += rating.overall_rating
                partner_data[rating.partner_type]['Service'] += rating.service
                partner_data[rating.partner_type]['Facilities'] += rating.facilities
                partner_data[rating.partner_type]['Cleanliness'] += rating.cleanliness
                partner_data[rating.partner_type]['Room'] += rating.room
                partner_data[rating.partner_type]['Value'] += rating.value
                partner_data[rating.partner_type]['Location'] += rating.location
                partner_data[rating.partner_type]['Food'] += rating.food
                partner_data[rating.partner_type]['Wifi'] += rating.wifi
                partner_data[rating.partner_type]['count'] += 1

            classification_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('classification').annotate(count=Count('classification'))   
            classification_counts_list = list(classification_counts)

            for item in classification_counts_list:
                cumulative_classification_counts[item['classification']] += item['count']


            source_counts = upload_data.objects.filter(OrganizationID=OrganizationID).values('source').annotate(count=Count('source'))  
            source_count_list = list(source_counts)
            for item in source_count_list:
                source_count_dict[item['source']] += item['count']

            review_list = upload_data.objects.filter(OrganizationID=OrganizationID).order_by('-reply_date')
            all_reviews.extend(review_list)
            
                
            total_counts['review_count'] += upload_data.objects.filter(OrganizationID=OrganizationID).count()
            total_counts['response_count'] += upload_data.objects.filter(OrganizationID=OrganizationID).exclude(Q(management_response__isnull=True) | Q(management_response__exact=np.nan) | Q(management_response=[])).count()
        if count_average > 0:
          total_averages = {k: round(v / count_average, 1) for k, v in total_averages.items()}
        final_averages = {key: round((sum(values) / len(values)) / 2, 1) for key, values in overall_averages.items() if values}
        for partner, values in partner_data.items():
            if values['count'] > 0:
                values['Overall_Rating'] /= values['count']
                values['Service'] /= values['count']
                values['Facilities'] /= values['count']
                values['Cleanliness'] /= values['count']
                values['Room'] /= values['count']
                values['Value'] /= values['count']
                values['Location'] /= values['count']
                values['Food'] /= values['count']
                values['Wifi'] /= values['count']

    

        

        total_dict = {
            "total_review": total_counts['review_count'],
            "total_response": total_counts['response_count']
        }
        
    
        return final_averages ,all_reviews,cumulative_classification_counts,source_count_dict,partner_data,total_dict

def clean_float_value(value):
    """Return None for nan values or invalid float values, otherwise return the value."""
    if pd.isna(value) or (isinstance(value, float) and pd.isna(value)):
        return None
    return value

def extract_external_responses(note):
    """Placeholder function for extracting external responses. Implement as needed."""
    # Example implementation, replace with your actual logic
    return [{'response_text': note}] if note else []
def excelFileData(f,OrganizationID,s):
    df1 = pd.read_excel(f, engine='openpyxl',skiprows=2)
    df2= pd.read_excel(s,engine='openpyxl',skiprows=2)
    df= pd.merge(df1, df2, on='Surveyid for internal use (e.g. RI link)', how='left')

    required_columns = [
    'Average Star Rating',
    'Response Date', 
    'NPS Segment - GSS', 
    'Likelihood to Recommend', 
    'Customer Service', 
    'Condition of Hotel',
    'Overall F&B Experience', 
    'Helpfulness of staff',
    'Overall Breakfast Experience',
    'Additional Feedback on Overall Stay', 
    'Social Media Source',
    'All Log Notes Combined (New Line)'
    ]
    df_filtered = df[required_columns]
    data = df_filtered.to_dict(orient='records')
    for row in data:
        note = row.get('All Log Notes Combined (New Line)')
        external_responses = extract_external_responses(note)
        management_response = [item['response_text'] for item in external_responses]
        classification_value = row.get('NPS Segment - GSS')
        classification_mapping = {
            'Detractors': 'Negative',
            'Detractors - Negative': 'Negative',
            'Passives': 'Neutral',
            'Promoters': 'Positive',
            'Promoters - Positive': 'Positive',
        }
        mapped_classification = classification_mapping.get(classification_value, 'Unknown')

        source_value=row.get('Social Media Source')
        source_mapping = {
        'AGODA': 'Agoda',
        'BOOKING': 'Booking.com',
        'GOOGLE_LOCAL': 'Google',
        'MAKE_MY_TRIP': 'MakeMyTrip',
        'TRIPADVISOR': 'Tripadvisor',
        }
        mapped_source = source_mapping.get(source_value, 'Unknown')
        def clean_and_divide(value):
            try:
                return float(value) / 2 if value is not None else None
            except (ValueError, TypeError):
                return None
        reply_date = None
        try:
            reply_date = pd.to_datetime(row.get['Response Date'], format='%d/%m/%Y', errors='coerce')
        except Exception as e:
                print(f"Error parsing reply_date: {e}")
        upload_data.objects.create(
            hotel= clean_and_divide(row.get('Average Star Rating')),
            service=clean_and_divide(row.get('Customer Service')),
            room=clean_and_divide(row.get('Likelihood to Recommend')),
            value=clean_and_divide(row.get('Overall F&B Experience')),
            cleanliness=clean_and_divide(row.get('Condition of Hotel')),
            classification=mapped_classification,
            review_text=row.get('Additional Feedback on Overall Stay'),
            management_response=management_response,
            reply_date=reply_date,
            source=mapped_source,
            OrganizationID=OrganizationID,
        )
   

def selectOrganization(request): 
    selected_org_id = None
    if request.GET.get('OrganizationID') :
        OrganizationID = request.GET.get('OrganizationID')
        selected_org_id=int(OrganizationID)
    
        averages ,review_list,classification_dict,source_dict,data,total_dict=dataShow(OrganizationID)
        
        if request.session["OrganizationID"] == "3":
            organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
        else:
            organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID)
        organization_choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in organizations]

    
        return render(request, 'review/display_data.html', {'averages': averages ,'reviewslist': review_list,"classification_counts":classification_dict,"source_counts":source_dict,'organization_choices': organization_choices,'data':data,'total_dict':total_dict,'selected_org_id':selected_org_id})

    else:
        return HttpResponse("No result for selected organization", status=400)
  
        
def extract_external_responses(text):
    if isinstance(text, str):
        pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] External response published: (.+)')
       
        matches = pattern.findall(text)
        
        results = []
        for match in matches:
            date_str, response_text = match
            published_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
            formatted_date = published_date.strftime('%d/%m/%Y')
            results.append({
                'published_date': formatted_date,
                'response_text': response_text.replace('_x000D_', '').strip()  # Clean up the response text
            })
        
        return results 
    else:
        return []



def feedback(request):
    try:
        OrganizationID = request.session.get('OrganizationID')
        if not OrganizationID:
            raise Exception("OrganizationID not found in session")
        review_list = upload_data.objects.filter(OrganizationID=OrganizationID).order_by('-reply_date')
    
        search = request.GET.get('search', '')
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')
        source = request.GET.get('source', '')
        reviewer = request.GET.get('search_guest', '')
        sentiment = request.GET.get('sentiment', '')
        if sentiment:
            positive_reviews = []
            negative_reviews = []
            neutral_reviews = []

            for feedback in review_list:
                blob = TextBlob(feedback.review_text)
                if blob.sentiment.polarity > 0:
                    positive_reviews.append(feedback)
                elif blob.sentiment.polarity < 0 :
                    negative_reviews.append(feedback)
                else :
                    neutral_reviews.append(feedback)


            if sentiment == 'Positive':
                review_list = positive_reviews
            elif sentiment == 'Negative':
                review_list = negative_reviews
            else:
                review_list = neutral_reviews

            if isinstance(review_list, list):
                review_ids = [feedback.id for feedback in review_list]
                review_list = upload_data.objects.filter(id__in=review_ids)
        

        if source:
            review_list = review_list.filter(source=source)
        if reviewer:
            review_list = review_list.filter(reviewer=reviewer)
        if search:
            review_list = review_list.filter(review_text__icontains=search)
        if from_date:
            review_list = review_list.filter(reply_date__gte=from_date)
        if to_date:
            review_list = review_list.filter(reply_date__lte=to_date)

        paginator = Paginator(review_list, 5)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
    
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            reviews = list(page_obj.object_list.values('review_title', 'source', 'review_text', 'management_response', 'reply_date'))
            return JsonResponse({
                'reviews': reviews,
                'total_pages': paginator.num_pages,
                'current_page': page_number
            })

        return render(request, 'review/feedback.html', {'reviews': page_obj})

    except Exception as e:
        print(f"Error in feedback view: {e}")  # Log the exception
        return render(request, 'review/feedback.html', {'error': str(e)})

@api_view(['GET'])
def upload_data_detail(request, OrganizationID=None):
    
    auth_header =request.META.get("HTTP_AUTHORIZATION")
    expected_token="So5gUf6ZbUHQU9SsP2j1Usx0PUCKA9gJJM2Kkgz7Fic0toLYTK14F2LKh4VXMBHR0sMKM0Y4WI7v71B8He5YdvM1YxsfKBJr6SXcJVUPrUC2owuerc61s3t29sETpzHKYvafTrk9JPs0x185ApQkr"
    token=""
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    if token == expected_token :   
        if request.method == 'GET':
            try:
                averages ,review_list,classification_dict,source_dict,data,total_dict=dataShow(OrganizationID)
                if OrganizationID == "3":
                    organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1)
                else:
                    organizations = OrganizationMaster.objects.filter(IsDelete=False, IsNileHotel=1, Activation_status=1, OrganizationID=OrganizationID)
                organization_choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in organizations]
                return render(request, 'review/review.html', {'averages': averages ,'reviewslist': review_list,"classification_counts":classification_dict,"source_counts":source_dict,'organization_choices': organization_choices,'data':data,'total_dict':total_dict})            
            except upload_data.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
    else:
       return HttpResponseForbidden()
            


def check_review_software(request, org_id):
    print("datta")
    organization = get_object_or_404(OrganizationMaster, OrganizationID=org_id)
    return JsonResponse({'reviewSoftware': organization.ReviewSoftware})
