from django.shortcuts import render

from django.shortcuts import render, redirect
from django.utils import timezone
from app.models import ModuleUserRights 
# Create your views here.

def User_Rights_View(request):
    context = {}
    return render(request, 'User_Rights_Module/User_Rights_Module.html', context)



def User_Rights_Form_Handle(request):
    pass



def User_Rights_Form_Handle(request):
    if request.method == "POST":
        UserID = request.POST.get("UserID")
        Module_Name = request.POST.get("Module_Name")
        Is_Access = request.POST.get("Is_Access") == "True"   # Convert string to boolean
        Is_Full_Access = request.POST.get("Is_Full_Access") == "True"

        # OrganizationID and CreatedBy from session (example)
        OrganizationID = request.session.get("OrganizationID", 0)
        CreatedBy = request.session.get("UserID", 0)

        # Save to DB
        ModuleUserRights.objects.create(
            UserID=UserID,
            Module_Name=Module_Name,
            Is_Access=Is_Access,
            Is_Full_Access=Is_Full_Access,
            OrganizationID=OrganizationID,
            CreatedBy=CreatedBy,
            CreatedDateTime=timezone.now()
        )

        return redirect("User_Rights_View")  # Redirect to same page after submit

    # If GET, load form
    return render(request, "User_Rights_Module/User_Rights_View.html")
