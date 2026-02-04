from rest_framework.decorators import api_view
from .serializers import HotelRatingSerializer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework import status
from .models import Hotel_Ranking
from django.utils import timezone
from datetime import date

# Create your views here.


def Ranking_Board_View(request):
    current_date = date.today().strftime("%Y-%m-%d")
    OrganizationID = request.session["OrganizationID"]
    
    context = {
        'current_date': current_date,
        'OrganizationID':OrganizationID
    }
    return render(request, "Ranking_Board/Rating_Board.html", context)


def Ranking_Board_Entry_View(request):
    Entry_Date = request.GET.get('Date')
    OrganizationID = request.session["OrganizationID"]
    Date_Flag = False
    if Entry_Date:
        current_date = Entry_Date
        Date_Flag = True
    else:
        current_date = date.today().strftime("%Y-%m-%d")
        Date_Flag = False
    context = {
        'current_date': current_date,
        'Date_Flag': Date_Flag,
        'OrganizationID':OrganizationID
    }
    return render(request, "Ranking_Board/Rating_Board_Entry.html", context)



@api_view(['GET', 'POST', 'PUT'])
def hotel_ranking_api(request):
    """
        GET: Retrieve hotel ratings (optionally filter by hotel or date)
        POST: Create a new rating
        PUT: Update an existing rating (based on HotelID + date)
    """

    if request.method == 'GET':
        hotel_id = request.GET.get('HotelID')
        date = request.GET.get('date')
        # S_OID = request.GET.get('S_OID')
        # UserID = request.GET.get('UserID')

        # print("organization id is here:=:", hotel_id, " --- ", type(hotel_id))

        if not hotel_id or not date:
            return Response({'error': 'OrganizationID and date are required'}, status=status.HTTP_400_BAD_REQUEST)

        ratings = Hotel_Ranking.objects.filter(IsDelete=False)
        if hotel_id != '3':
            ratings = ratings.filter(HotelID=hotel_id)

        if date:
            ratings = ratings.filter(date=date)

        serializer = HotelRatingSerializer(ratings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        UserID = request.GET.get('UserID') or 0
        S_OID = request.GET.get('S_OID') or 0

        data = request.data
        # data['CreatedBy'] = UserID
        # data['OrganizationID'] = S_OID
        # serializer = HotelRatingSerializer(data=data, many=True)

        if isinstance(data, list):
            for item in data:
                item['CreatedBy'] = int(UserID)
                item['OrganizationID'] = S_OID
            serializer = HotelRatingSerializer(data=data, many=True)
        else:
            data['CreatedBy'] = int(UserID)
            data['OrganizationID'] = S_OID
            serializer = HotelRatingSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"error": "The data is already exist"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    elif request.method == 'PUT':
        UserID = request.GET.get('UserID') or 0
        data = request.data  # This will be a list of hotel data objects

        if not isinstance(data, list):
            return Response({'error': 'Expected a list of records'}, status=status.HTTP_400_BAD_REQUEST)

        updated_records = []

        for item in data:
            hotel_id = item.get('HotelID')
            date = item.get('date')

            if not hotel_id or not date:
                continue  # Skip invalid items

            try:
                # Find existing record for this HotelID + Date
                rating_instance = Hotel_Ranking.objects.get(
                    HotelID=hotel_id,
                    date=date,
                    IsDelete=False
                )
            except Hotel_Ranking.DoesNotExist:
                continue  # Skip if not found (you can also choose to create new)

            item['ModifyBy'] = int(UserID)
            item['ModifyDateTime'] = timezone.now()

            serializer = HotelRatingSerializer(rating_instance, data=item, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_records.append(serializer.data)

        if not updated_records:
            return Response({'error': 'No matching records found to update'}, status=status.HTTP_404_NOT_FOUND)

        return Response(updated_records, status=status.HTTP_200_OK)
