from app.models import OrganizationMaster


class MasterAttribute:
    CurrentHost="http://localhost:50970"
    Host = "https://hotelops.in"
    DomainCode = ""
    PyHost = "http://hotelops.in:8080/"
    Logout = "hotelops.in/Home/Logout?Token="
    HomeURL = "hotelops.in{{request.session.HomeURL}}?Token="
    ChangePassword = "hotelops.in{{request.session.ChangePassword}}?Token="
    MonthList=["","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    HotelAPIkeyToken="WfEj45ON8BKl!udLGPu!szcWtY!e9MTm4jpXSqD7wNM1HITpnbJhhp=aElxgkShcdaBhvgqLeOMjz9G?qliY6FK/AcJN0iTB3fIl5g55bllJHdrF-Yh-O4W-eEjKaPk/DBGqHU6XDhbG5m68RtVxZGH?B6n1F5u=F84npBeJIMS/SzrT7=dXuAj=8aqDyvRpIh=nswd!XPTMobzhw2jKxocrOYJkzo0osZFSMxK1hMqRbqGJIKR=bgRfS!cea2fb"
    azure_storage_account_key = "gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A=="
    azure_storage_account_name = "hotelopsdevstorage"
    azure_connection_string = "DefaultEndpointsProtocol=https;AccountName=hotelopsdevstorage;AccountKey=gH5NXveEI5+AlwbwjBqGLj14u8Il9QLdsr8aarLlFp8gSPRDxdrW8CWTw34yhmpGdJXJlJFCELOY+AStEL/i4A==;BlobEndpoint=https://hotelopsdevstorage.blob.core.windows.net/;QueueEndpoint=https://hotelopsdevstorage.queue.core.windows.net/;TableEndpoint=https://hotelopsdevstorage.table.core.windows.net/;FileEndpoint=https://hotelopsdevstorage.file.core.windows.net/;"
    OrganizationLogoURL = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"
    NileLogoURL = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/NileWhite.jpg"
    storage_account_key = "PV6pykN3d/a4jjH64vEd4qsQUGQuohDthY2JUGN9z5+9EmoGBJpabNShKP0rJOAxWj5kvwAXD1BPUUUSUZgSfg=="
    storage_account_name = "hotelopsblob"
    connection_string = "AccountName=hotelopsblob;AccountKey=PV6pykN3d/a4jjH64vEd4qsQUGQuohDthY2JUGN9z5+9EmoGBJpabNShKP0rJOAxWj5kvwAXD1BPUUUSUZgSfg==;DefaultEndpointsProtocol=http;BlobEndpoint=https://hotelopsblob.blob.core.windows.net/;QueueEndpoint=https://hotelopsblob.queue.core.windows.net/;TableEndpoint=https://hotelopsblob.queue.core.windows.net/;"



class OrganizationDetail:
    def __init__(self, OrganizationID):
        # Initialize attributes with default values
        self.OrganizationID = OrganizationID
        self.OrganizationName = ""
        self.OrganizationLogo = ""
        self.OrganizationDomainCode = ""
        self.ShortDisplayLabel = ""
        self.Address = ""
        self.Activation_status = ""
        self.IsNileHotel = None
        self.FinancialYearStart = None
        self.GSTNumber = ""
        self.MComLogo = True
        
        # Retrieve organization details from the model
        try:
            organization = OrganizationMaster.objects.get(OrganizationID=OrganizationID)
            self.OrganizationName = organization.OrganizationName
            self.OrganizationLogo = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/" + organization.OrganizationLogo
            self.OrganizationDomainCode = organization.OrganizationDomainCode
            self.ShortDisplayLabel = organization.ShortDisplayLabel
            self.Address = organization.Address
            self.Activation_status = organization.Activation_status
            self.IsNileHotel = organization.IsNileHotel
            self.FinancialYearStart = organization.FinancialYearStart
            self.GSTNumber = organization.GSTNumber
            self.MComLogo = organization.MComLogo
        except OrganizationMaster.DoesNotExist:
            # Handle the case where the organization does not exist in the database
            pass

    def get_OrganizationName(self):
        return self.OrganizationName

    def get_OrganizationLogo(self):
        return self.OrganizationLogo

    def get_OrganizationDomainCode(self):
        return self.OrganizationDomainCode

    def get_ShortDisplayLabel(self):
        return self.ShortDisplayLabel

    def get_Address(self):
        return self.Address

    def get_Activation_status(self):
        return self.Activation_status

    def get_IsNileHotel(self):
        return self.IsNileHotel

    def get_FinancialYearStart(self):
        return self.FinancialYearStart

    def get_GSTNumber(self):
        return self.GSTNumber

    def get_MComLogo(self):
        return self.MComLogo
    
    def get_Organization_name(self):
        return self.OrganizationName

# class OrganizationDetail:
#     def __init__(self, OrganizationID):
#         # Initialize attributes with default values
#         self.OrganizationID = OrganizationID
#         self.Organization_name = ""
#         self.OrganizationLogo = ""
#         self.OrganizationDomainCode = ""
#         self.ShortDisplayLabel = ""
        
#         # Retrieve user details from the model
#         try:
#             user = OrganizationMaster.objects.get(OrganizationID=OrganizationID)
#             self.Organization_name = user.Organization_name  # Replace 'username' with the actual field name
#             self.OrganizationLogo = "https://hotelopsblob.blob.core.windows.net/hotelopslogos/"+user.OrganizationLogo  # Replace 'full_name' with the actual field name
#             self.OrganizationDomainCode = user.OrganizationDomainCode  # Replace 'full_name' with the actual field name
#             self.ShortDisplayLabel = user.ShortDisplayLabel  # Replace 'full_name' with the actual field name
#         except OrganizationMaster.DoesNotExist:
#             # Handle the case where the user does not exist in the database
#             pass

#     def get_Organization_name(self):
#         return self.Organization_name

#     def get_OrganizationLogo(self):
#         return self.OrganizationLogo
#     def get_OrganizationDomainCode(self):
#         return self.OrganizationDomainCode
#     def get_ShortDisplayLabel(self):
#         return self.ShortDisplayLabel
    