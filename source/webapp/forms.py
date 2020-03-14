from django import forms
from django.forms import ClearableFileInput
from webapp.models import File


class FileForm(forms.ModelForm):

    class Meta:
        model = File
        exclude = ['created_by', 'downloaded']


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')

