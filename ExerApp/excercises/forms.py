from django import forms 

from .models import ItemBase, Content, Text, BlankText, Exercise, ExerciseSet


class ExerciseSetCreationForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['name','description','is_public']
        labels = {
            "is_public":"Make this set public"
        }

class ExerciseSetPublicStatus(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['is_public']
        labels = {
            "is_public":"Make this set public"
        }

