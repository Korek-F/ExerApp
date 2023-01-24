from django import forms 
from django.core.validators import MinLengthValidator
from .models import Category 
from excercises.models import ExerciseSet
from django.shortcuts import get_object_or_404

class CreateCategoryForm(forms.Form):
    name = forms.CharField()
    set_id = forms.IntegerField(widget=forms.HiddenInput())

    def clean_name(self):
        name = self.cleaned_data["name"]
        return name.upper().strip()
    
    def clean(self):
        super(CreateCategoryForm,self).clean()
        self.exercise_set = get_object_or_404(ExerciseSet, id=self.cleaned_data["set_id"])
        if not self.exercise_set.categories.count()<5:
            self._errors["name"] = self.error_class(["You can't add more thant 5 categories"])
        
        if len(self.cleaned_data["name"])<3:
            self._errors["name"] = self.error_class(["Category name is too short!"])
        return self.cleaned_data
    
    def save(self):
        data = self.cleaned_data 
        category,created = Category.objects.get_or_create(name=data["name"])
        self.exercise_set.categories.add(category)
        self.exercise_set.save()
        return category