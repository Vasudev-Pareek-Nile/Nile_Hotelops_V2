from django import forms

class AlifFileUploadForm(forms.Form):
    file = forms.FileField()
