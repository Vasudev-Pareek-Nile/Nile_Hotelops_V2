from rest_framework.permissions import BasePermission

class HasValidUserAndOrgID(BasePermission):
    # ALLOWED_USER_IDS = ["100"]
    ALLOWED_USER_IDS = ["20201212178780", "20201212180048"]
    ALLOWED_ORG_IDS = ["3"]

    def has_permission(self, request, view):
        user_id = request.query_params.get('UserID')
        org_id = request.query_params.get('OID')
        return user_id in self.ALLOWED_USER_IDS and org_id in self.ALLOWED_ORG_IDS
