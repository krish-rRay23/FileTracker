from django import forms
from .models import *
from django.contrib.auth.models import User

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['unique_id', 'file_name']

class PassFileForm(forms.Form):
    passed_to = forms.ModelChoiceField(queryset=User.objects.all())
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']  # Ensure 'text' is included here