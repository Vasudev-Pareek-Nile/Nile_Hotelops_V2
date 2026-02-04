from rest_framework import serializers
from .models import OpenPosition
from app.models import OrganizationMaster
from .utils import generate_position_image

from Job_Description.models import JobDescription
from rest_framework import serializers
from .models import CareerResume

class CareerResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerResume
        fields = '__all__'  

class OpenPositionSerializer(serializers.ModelSerializer):
    days_ago = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    url_slug = serializers.SerializerMethodField()
    organization_logo = serializers.SerializerMethodField()
    logo_image = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    share_image = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()    

    class Meta:
        model = OpenPosition
        fields = [
            'organization_logo',
            'logo_image',
            'id',
            'job_title',
            'url_slug',
            'Position',
            'OpenDepartment',
            'Job_Type',
            'salary',
            'Locations',
            'Number',
            'Opened_On',
            'Status',
            'days_ago',
            'description',
            'share_image',  
        ]

    def get_days_ago(self, obj):
        return obj.days_ago()

    def get_job_title(self, obj):
        return obj.job_title()
    
    def get_salary(self, obj):
        return obj.get_formatted_salary()

    def get_url_slug(self, obj):
        return obj.url_slug()

    def get_organization_logo(self, obj):
        try:
            organization = OrganizationMaster.objects.get(OrganizationDomainCode=obj.Locations)
            return organization.OrganizationLogo.name
        except OrganizationMaster.DoesNotExist:
            return None

    def get_logo_image(self, obj):
        try:
            organization = OrganizationMaster.objects.get(OrganizationDomainCode=obj.Locations)
            if organization.OrganizationLogo:
                return f"https://hotelopsblob.blob.core.windows.net/hotelopslogos/{organization.OrganizationLogo.name}"
        except OrganizationMaster.DoesNotExist:
            return None

    def get_description(self, obj):
        
        return f"If you are looking for a job as {obj.job_title()} at {obj.Locations}, apply now!"

    def get_share_image(self, obj):
        try:
            image_url = generate_position_image(obj.Position, obj.url_slug(), obj.Locations)
            return image_url
        except Exception as e:
            
            print(f"An error occurred: {e}")
            return None



from rest_framework import serializers
from .models import OpenPosition

from rest_framework import serializers
from .models import JobDescription

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = [
            'Job_Scope',
            'Duties_Responsibilities',
            'Job_Knowledge_Skills',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        combined_description = f"""
        <div>
            <h3>Job Scope</h3>
            {representation['Job_Scope']}
            <h3>Duties & Responsibilities</h3>
            {representation['Duties_Responsibilities']}
            <h3>Job Knowledge & Skills</h3>
            {representation['Job_Knowledge_Skills']}
        </div>
        """
        return {'content': combined_description}

from rest_framework import serializers
from .models import OpenPosition

from rest_framework import serializers
from .models import OpenPosition, JobDescription, OrganizationMaster

class JobDetailsSerializer(serializers.ModelSerializer):
    Position = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()
    og_title = serializers.SerializerMethodField()
    og_description = serializers.SerializerMethodField()
    canonical_url = serializers.SerializerMethodField()
    og_url = serializers.SerializerMethodField()
    logo_image = serializers.SerializerMethodField()
    share_image = serializers.SerializerMethodField()
    red_url = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    full_location_name = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    Address = serializers.SerializerMethodField()
    Hotel_Location = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()
    class Meta:
        model = OpenPosition
        fields = [
            'Position',
            'og_title',
            'og_description',
            'description',
            'canonical_url',
            'og_url',
            'logo_image',
            'share_image',
            'red_url',
            'Number',
            
            'salary',
            'Opened_On',
            'OpenDepartment',
            'full_location_name',
            'content',
            'job_title',
            'title',
            'Address',
            'Hotel_Location',
        ]
    def get_Position(self, obj):
        return f"{obj.Position} position is available at {obj.get_full_location_name()}. This is a {obj.Job_Type} job under {obj.OpenDepartment}. Easily apply for this job."

    def get_og_title(self, obj):
        return f"{obj.Position} position is available at {obj.get_full_location_name()}. This is a {obj.Job_Type} job under {obj.OpenDepartment}. Easily apply for this job."

    def get_og_description(self, obj):
        return f"{obj.Position} position is available at {obj.get_full_location_name()}. This is a {obj.Job_Type} job under {obj.OpenDepartment}. Easily apply for this job."

    def get_canonical_url(self, obj):
        return f"https://careersatnile.com/job-description.php?job-title={obj.url_slug()}"

    def get_og_url(self, obj):
        return self.get_canonical_url(obj)

    def get_logo_image(self, obj):
        return obj.logo_image()
    
    def get_salary(self, obj):
        return obj.get_formatted_salary()


    def get_share_image(self, obj):
        return f"https://hotelopsblob.blob.core.windows.net/nilecareer/0/{obj.PositionImage}"

    def get_red_url(self, obj):
        return f"https://careersatnile.com/jobshare.php/{obj.url_slug()}"

    def get_content(self, obj):
        try:
            job_description = JobDescription.objects.get(Position=obj.Position)
            return JobDescriptionSerializer(job_description).data['content']
        except JobDescription.DoesNotExist:
            return None

    def get_full_location_name(self, obj):
        
        return obj.get_full_location_name()

    def get_job_title(self, obj):
        return f"{obj.Position} - {obj.OpenDepartment}"

    def get_title(self, obj):
        return f"New Job Opening - {obj.Position} - {obj.OpenDepartment}"

    def get_Address(self, obj):
        try:
            
            print(f"Looking up OrganizationMaster with name: {obj.Locations}")
           
            organization = OrganizationMaster.objects.get(OrganizationName__iexact=obj.Locations)
            
            
            return organization.Address
        except OrganizationMaster.DoesNotExist:
           
            print(f"OrganizationMaster with name {obj.Locations} not found.")
            return None

    def get_Hotel_Location(self, obj):
        try:
            
            print(f"Looking up OrganizationMaster with name: {obj.Locations}")
           
            organization = OrganizationMaster.objects.get(OrganizationName__iexact=obj.Locations)
            
            
            return organization.Hotel_Location
        except OrganizationMaster.DoesNotExist:
           
            print(f"OrganizationMaster with name {obj.Locations} not found.")
            return None
        
       
        
from .utils import get_organization_Shortname_name_from_location
from django.utils import timezone

class OpenPositionMobileSerializer(serializers.ModelSerializer):
    htl_name = serializers.SerializerMethodField()
    since_days = serializers.SerializerMethodField()

    class Meta:
        model = OpenPosition
        fields = (
            "id",
            "htl_name",
            "Position",
            "OpenLevel",
            "OpenDivision",
            "OpenDepartment",
            "Locations",
            "Opened_On",
            "since_days",
        )

    def get_htl_name(self, obj):
        return get_organization_Shortname_name_from_location(obj.Locations)

    def get_since_days(self, obj):
        if not obj.Opened_On:
            return None

        today = timezone.now().date()
        opened_on = obj.Opened_On

        return (today - opened_on).days