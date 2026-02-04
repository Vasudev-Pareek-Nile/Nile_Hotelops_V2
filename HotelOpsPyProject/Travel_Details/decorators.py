from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from hotelopsmgmtpy.GlobalConfig import MasterAttribute

ALLOWED_USER_IDS = ["20201212178780", "20201212180048"]

def user_id_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user_id = str(request.session.get("UserID"))
        if user_id not in ALLOWED_USER_IDS:
            messages.error(request, "You are not authorized to access this page.")
            return redirect(MasterAttribute.Host)  # or another page
        return view_func(request, *args, **kwargs)
    return _wrapped_view
