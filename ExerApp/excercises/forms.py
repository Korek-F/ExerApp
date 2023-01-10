from django import forms 

from .models import ItemBase, Content, Text, BlankText, Exercise, ExerciseSet


class ExerciseSetCreationForm(forms.ModelForm):
    class Meta:
        model = ExerciseSet
        fields = ['name']