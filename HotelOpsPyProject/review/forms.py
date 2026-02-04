# myapp/forms.py
from django import forms
from app.models import OrganizationMaster
from .models import upload_data

class UploadFileForm(forms.Form):
    file = forms.FileField(required=True, label='Primary File')
    second_file = forms.FileField(required=False, label='Secondary File')
    date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(2000, 2031)), 
        label='Date'
    )
    OrganizationID = forms.ChoiceField(choices=[], label='Organization Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['OrganizationID'].choices = self.get_organization_choices()

    def get_organization_choices(self):
        choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in OrganizationMaster.objects.all()]
        return choices

    def clean(self):
        cleaned_data = super().clean()
        organization_id = cleaned_data.get('OrganizationID')
        file = cleaned_data.get('file')
        second_file = cleaned_data.get('second_file')

        if organization_id:
            try:
                organization = OrganizationMaster.objects.get(OrganizationID=organization_id)
            except OrganizationMaster.DoesNotExist:
                self.add_error('OrganizationID', 'Selected organization does not exist.')
                return cleaned_data

            if organization.ReviewSoftware == "reviewPro" or organization.ReviewSoftware == "Rankly":
                if not file:
                    self.add_error('file', 'Primary file is required')
            else:
                if not file:
                    self.add_error('file', 'Primary file is required')
                if not second_file:
                    self.add_error('second_file', 'Secondary file is required')

        return cleaned_data
class OrganizationSelectionForm(forms.Form):
    OrganizationID = forms.ChoiceField(choices=[], label='Organization Name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['OrganizationID'].choices = self.get_organization_choices()

    def get_organization_choices(self):
        choices = [(org.OrganizationID, org.ShortDisplayLabel) for org in OrganizationMaster.objects.all()]
        return choices
