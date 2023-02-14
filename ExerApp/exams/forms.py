from django import forms 
from .models import ExamSession, Exam

class SessionForm(forms.ModelForm):
    class Meta:
        model = ExamSession
        fields = ['user_name']

class CreateExamForm(forms.ModelForm):

    def clean(self):
        super(CreateExamForm,self).clean()
        if len(self.cleaned_data["name"])<3:
            self._errors["name"] = self.error_class(["The exam name is too short!"])

        if self.cleaned_data["start_at"] and self.cleaned_data["end_at"]:
            if self.cleaned_data["start_at"]>self.cleaned_data["end_at"]:
                self._errors["start_at"] = self.error_class(["The exam start time can't be later than the end time!"])
                self._errors["end_at"] = self.error_class(["The exam end time can't be earlier than the start time!"])
        return self.cleaned_data

    class Meta:
        model = Exam
        fields = ['name','description','start_at','end_at']
        widgets = {
        'start_at': forms.DateInput(format=('%H:%i:%s %m/%d/%Y'), attrs={ 'type':'datetime-local'}),
        'end_at': forms.DateInput(format=('%H:%i:%s %m/%d/%Y'), attrs={ 'type':'datetime-local'}),
    }