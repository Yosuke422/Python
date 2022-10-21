from django import forms
from .models import list
 
 
class list(forms.ModelForm):
 
    class Meta:
        
        model = list
        fields = [
            "title",
            "description",
        ]