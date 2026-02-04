from django.urls import path
from  .import  views 
urlpatterns = [
       path('agreement_add/',views.agreement_add,name="agreement_add"),
       path('agreement_list/',views.agreement_list,name="agreement_list"), 
       path('agreement_delet/',views.agreement_delet,name="agreement_delet"),

# master add urls

        path('master_list/',views.master_list,name="master_list"), 
        path('master_add/',views.master_add,name="master_add"),
        path('master_delete/',views.master_delete,name="master_delete"),

# Sub article master add urls
     path('sub_articlelist/',views.sub_articlelist,name="sub_articlelist"),
     path('sub_articleadd/',views.sub_articleadd,name="sub_articleadd"),
     path('sub_delete/',views.sub_delete,name="sub_delete"),
# child article master add urls
     path('child_articlelist/',views.child_articlelist,name="child_articlelist"),
     path('Child_articleadd/',views.Child_articleadd,name="Child_articleadd"),
     path('child_delete/',views.child_delete,name="child_delete"),

# view  article master add urls
     path('view_agreement/',views.view_agreement,name="view_agreement"),
     path('agreement_pdf/',views.agreement_pdf,name="agreement_pdf"),

# agreement uploded urls
    path('agreement_uploded/',views.agreement_uploded,name="agreement_uploded"),


     path('subchild/',views.subchild,name="subchild"),
      path('subchild_list/',views.subchild_list,name="subchild_list"),
      path('subchild_delet/',views.subchild_delet,name="subchild_delet"),
      
      

]
