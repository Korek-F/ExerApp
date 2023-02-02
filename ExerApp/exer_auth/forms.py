from django import forms 
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserCreationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username','password1','password2','email']:
            self.fields[fieldname].help_text=None

    class Meta:
        model = User 
        fields = ['username','email','password1','password2']
