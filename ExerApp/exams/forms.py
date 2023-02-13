from django import forms 
from .models import ExamSession

class SessionForm(forms.ModelForm):
    class Meta:
        model = ExamSession
        fields = ['user_name']