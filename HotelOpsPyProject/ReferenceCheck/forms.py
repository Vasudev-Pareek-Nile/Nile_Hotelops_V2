from django import forms
from django.contrib.auth.models import User
from . import models

#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        

class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class RadioInput(forms.RadioSelect):
    input_type = 'radio'



class ReferenceCkeckForm(forms.ModelForm):
    class Meta:
        model=models.Reference_Registration_Form
        fields=['Applicant_Name','From','To','Referee_Company_Name','Final_Position','Refeere_Name','Did_You_Directly_Supervise','Refeere_Position','Refeere_Phone_No','Overall_Performance','Strenght','Weaknesses',
                'What_is_Best_Way_To_Manage_This_Candidate','What_Would_His_Supervisor_Say_About_Him','What_Would_His_Peers_Say_About_Him','Development_Areas','Reason_For_Leaving','Would_You_ReHire_This_Person','Checked_By','Date',"OrganizationID","CreatedBy"]
        widgets = {
            'From': DateInput,
            'To': DateInput,
            'Date': DateInput,
            # 'Resignation_Letter':RadioInput,
            # 'Acc_Of_Resign':RadioInput,
            # 'Notice_Period_Served':RadioInput,
            # 'Notice_Period_Waived_Off':RadioInput,
            # 'Exit_Interview_By_Hr':RadioInput,
            # 'Full_And_Final_Settlement':RadioInput,  
        } 