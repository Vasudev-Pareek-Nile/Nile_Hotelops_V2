from django import forms
from .models import Media_Asset_Library

class MediaAssetLibraryForm(forms.ModelForm):
    class Meta:
        model = Media_Asset_Library
        fields = '__all__'
