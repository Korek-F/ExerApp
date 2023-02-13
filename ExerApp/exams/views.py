from django.shortcuts import render, get_object_or_404, redirect
from django.views import  View
from .models import Exam, ExamSession, SessionAnswer
from excercises.models import Content
from .forms import SessionForm
from .utils import check_session_answers
from excercises.utils import render_checked_exercise
from django.utils import timezone

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

            return render(request, 'exams/partials/session_link.html',{"session":obj})

        return render(request, 'exams/partials/start_session_form.html',context)

class SessionView(View):
    def get(self, request, slug):
        session = get_object_or_404(ExamSession, slug=slug)
        context={
            "is_ready": session.exam.start_at<timezone.now(),
            "session":session
        }
        return render(request, 'exams/session.html',context)
    
    def post(self,request,slug):
        session = get_object_or_404(ExamSession, slug=slug)
        context={
            "session":session
        }
        for i in request.POST:
            if i.startswith(('answer_blank','answer_abcd')):
                obj_id = int(i.split("_")[2])
                obj = get_object_or_404(Content, pk=obj_id)
                answer = request.POST[i].strip()
                SessionAnswer.objects.create(exam_session=session, item=obj, user_answer=answer)
        session.is_finished = True 
        session.save()
        return render(request, 'exams/partials/session_result.html',context)

class SessionResultsView(View):
    def get(self,request,slug):
        session = get_object_or_404(ExamSession, slug=slug)
        context={"session":session}
        if session.exam.end_at > timezone.now():
            return render(request, 'exams/partials/exam_is_not_ended.html', context)

        correct_items, wrong_items = check_session_answers(session)
        checked_answers = []
        for exercise in session.exam.exercise_set.exercise_set.all():
            checked_exercise = render_checked_exercise(exercise, correct_items, wrong_items)
            checked_answers.append(checked_exercise)
        correct_ratio = (len(correct_items)/session.exam.exercise_set.number_of_points)*100
        context = {
            'checked_answers': checked_answers,
            "correct_ratio":correct_ratio}

        return render(request, 'exams/partials/session_checked_results.html', context)

