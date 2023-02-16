from django.shortcuts import render, get_object_or_404, redirect
from django.views import  View
from .models import Exam, ExamSession, SessionAnswer
from excercises.models import ExerciseSet
from excercises.models import Content
from .forms import SessionForm, CreateExamForm
from .utils import get_rendered_answers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q
from django.utils import timezone

# Create your views here.
class StartExamView(View):
    def get(self,request, slug):
        exam = get_object_or_404(Exam, slug=slug)
        form = SessionForm()
        context={
            'form':form,
            "exam":exam,
        }
        context["is_ended"]= exam.is_ended
        
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
            return render(request, 'exams/partials/session_link.html',{"session":obj})

        return render(request, 'exams/partials/start_session_form.html',context)

class SessionView(View):
    def get(self, request, slug):
        session = get_object_or_404(ExamSession, slug=slug)
        context={
            "session":session,
            'is_ready':session.exam.is_started
        }
        if session.is_finished:
            return render(request, 'exams/results.html',context)
        
        return render(request, 'exams/session.html',context)
    
    def post(self,request,slug):
        session = get_object_or_404(ExamSession, slug=slug)
        context={"session":session}
        for i in request.POST:
            if i.startswith(('answer_blank','answer_abcd')):
                obj_id = int(i.split("_")[2])
                obj = get_object_or_404(Content, pk=obj_id)
                answer = request.POST[i].strip()
                SessionAnswer.objects.create(exam_session=session, item=obj, user_answer=answer)
        session.is_finished = True 
        session.end_at = timezone.now()
        session.save()
        return render(request, 'exams/partials/session_result.html',context)

class SessionResultsView(View):
    def get(self,request,slug):
        session = get_object_or_404(ExamSession, slug=slug)
        context={"session":session}
        if not session.exam.is_ended and session.exam.end_at:
            return render(request, 'exams/partials/exam_is_not_ended.html', context)

        correct_items, checked_answers, correct_ratio = get_rendered_answers(session)
        context = {
            'checked_answers': checked_answers,
            "correct_ratio":correct_ratio}

        session.points = len(correct_items)
        session.save()

        return render(request, 'exams/partials/session_checked_results.html', context)


class CreateExamView(LoginRequiredMixin, View):
    def get(self,request,id):
        exercise_set = get_object_or_404(ExerciseSet, pk=id)
        context = {
            'form':CreateExamForm(),
            'exercise_set':exercise_set
        }
        return render(request, 'exams/create_exam.html', context)
    def post(self,request,id):
        exercise_set = get_object_or_404(ExerciseSet, pk=id)
        form = CreateExamForm(request.POST or None)
        context ={'form':form,"exercise_set":exercise_set}
        if form.is_valid():
            obj = form.save(commit=False)
            obj.exercise_set = exercise_set
            obj.owner = request.user
            obj.save()
            context["exam"]=obj
            return render(request, 'exams/partials/exam_created.html', context)
        return render(request, 'exams/partials/create_exam_form.html', context)

class ExamListView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request, 'exams/exam_list.html')

class ExamOwnerView(LoginRequiredMixin, View):
    def get(self,request, slug):
        exam = get_object_or_404(Exam, slug=slug)
        if request.user != exam.owner:
            return redirect("exercises")
        context = {"exam":exam}
        return render(request, 'exams/exam_details.html', context)

class SessionDetailView(LoginRequiredMixin, View):
    def get(self,request,slug):
        session = get_object_or_404(ExamSession, slug=slug)
        if request.user != session.exam.owner:
            return redirect("exercises")

        correct_items, checked_answers, correct_ratio = get_rendered_answers(session)

        context = {"session":session,
        "checked_answers":checked_answers,
        "correct_ratio":correct_ratio}

        return render(request, 'exams/session_details.html', context)
    
class SearchExamsView(ListView):
    model = Exam
    template_name = "exams/partials/searched_exams.html"
    

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Exam.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()
        return object_list