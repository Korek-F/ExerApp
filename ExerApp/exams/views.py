from django.shortcuts import render, get_object_or_404
from django.views import  View
from .models import Exam, ExamSession
from .forms import SessionForm

# Create your views here.
class StartExamView(View):
    def get(self,request, slug):
        exam = get_object_or_404(Exam, slug=slug)
        form = SessionForm()
        context={
            'form':form,
            "exam":exam
        }
        return render(request, 'exams/start_session.html',context)
    
    def post(self,request, slug):
        exam = get_object_or_404(Exam, slug=slug)
        form = SessionForm(request.POST)
        context={
            'form':form,
            "exam":exam
        }
        if form.is_valid():
            obj = form.save(commit=False)
            obj.exam = exam
            obj.save()
        return render(request, 'exams/start_session.html',context)