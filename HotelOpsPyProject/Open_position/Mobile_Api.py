from .serializers import OpenPositionMobileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework import status
from .models import OpenPosition
from datetime import timedelta

import logging


logger = logging.getLogger(__name__)


class Open_Position_List_Mobile_API(APIView):
    """
    GET → List Open Positions
    """

    def get(self, request):
        Session_division_name = request.GET.get("divi_name")
        Session_OID = request.GET.get("SessionOID")
        UserType = request.GET.get("UserType", '').lower()
        OID = request.GET.get("OID")
        raw_levels = request.GET.getlist("Level")

        Levels = []
        for lvl in raw_levels:
            Levels.extend(lvl.split(","))

        Levels = [lvl.strip() for lvl in Levels if lvl.strip()]
        # thirty_days_ago = timezone.now() - timedelta(days=100)
        hundred_days_ago = timezone.now() - timedelta(days=100)


        if Session_OID == "3" and OID == "333333":
            queryset = OpenPosition.objects.filter(
                IsDelete=False,
                CreatedDateTime__gte=hundred_days_ago
            ).order_by("-CreatedDateTime")
        else:
            queryset = OpenPosition.objects.filter(
                IsDelete=False,
                CreatedDateTime__gte=hundred_days_ago,
                Locations=OID
            ).order_by("-CreatedDateTime")

        if Levels:
            queryset = queryset.filter(OpenLevel__in=Levels)

        # if UserType != 'ceo':
        #     if Session_division_name:
        #         queryset = queryset.filter(OpenDivision=Session_division_name)
                
        #     if Session_division_name:
        #         Session_division_name = Session_division_name.strip()
        #         queryset = queryset.filter(OpenDivision__iexact=Session_division_name)

        # Division filter (skip for CEO)
        # if UserType != "ceo" and Session_division_name:
        if UserType not in ('ceo', 'gm', 'hr') and Session_division_name:
            print("iam at ceo restirct area")
            queryset = queryset.filter(
                OpenDivision__iexact=Session_division_name.strip()
            )

        queryset = queryset.order_by("-CreatedDateTime")
        
        serializer = OpenPositionMobileSerializer(queryset, many=True)

        return Response({
            "status": True,
            "count": queryset.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

