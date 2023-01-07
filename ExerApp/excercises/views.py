from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import ExerciseSet, BlankText,Exercise, Text, Content, Hint
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect


def mainpage(request):
    return HttpResponse("Hello world!")


class ExerciseSetDetailView(View):
    def get(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        context = {'exercise_set': exercise_set}
        return render(request, 'excercises/excercise_set_page.html', context)



class ExerciseSetEditView(View):
    def get(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        
        context = {'exercise_set': exercise_set,  
        'count':len(exercise_set.exercise_set.all())}
        
        return render(request,'excercises/excercise_set_edit.html',context)
    
    def post(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        current_ex_number = -1
        current_ex = None
        for i in request.POST:
            if i.startswith("content"):
                _, content_type,ex_number,content_number = i.split("-")
                if current_ex_number !=ex_number:
                    current_ex = Exercise.objects.create(exercise_set=exercise_set)
                    current_ex_number =ex_number
                if content_type=="Text":
                    content_item = Text.objects.create(content=request.POST[i])
                    cc = ContentType.objects.get_for_model(Text)
                    Content.objects.create(exercise=current_ex, content_type=cc,object_id=content_item.id)
                elif content_type=="Blank":
                    content_item = BlankText.objects.create(correct=request.POST[i])
                    cc = ContentType.objects.get_for_model(BlankText)
                    Content.objects.create(exercise=current_ex, content_type=cc,object_id=content_item.id)
                elif content_type=="Hint":
                    content_item = Hint.objects.create(content=request.POST[i])
                    cc = ContentType.objects.get_for_model(Hint)
                    Content.objects.create(exercise=current_ex, content_type=cc,object_id=content_item.id)
                

        return HttpResponseRedirect(request.path_info)

class ExerciseSetLearnView(View):
    def get(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        context = {'exercise_set': exercise_set}
        return render(request,'excercises/excercise_set_learn.html',context)

class ExerciseSetCheckView(View):
    def post(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])

        correct_items = []
        wrong_items = {}
        for i in request.POST:
            if i.startswith('answer'):
                obj_id = int(i.split("_")[2])
                obj = get_object_or_404(BlankText, pk=obj_id)
                answer = request.POST[i]
                if obj.isCorrect(answer):
                    correct_items.append(obj)
                else:
                    wrong_items[obj]=answer
        
        checked_answers = []
        for exercise in exercise_set.exercise_set.all():
            checked_exercise = []
            for content in exercise.content_set.all():
                if content.item.content_type != 'text':

                    if not content.item in correct_items:
                        answer = wrong_items[content.item]
                        if answer == '':
                            answer="___"
                        checked_exercise.append(render_to_string('excercises/checked_exercises/wrong.html',{"correct":content.item.correct_answer,
                        "answer":answer}
                         ))

                    else:
                        checked_exercise.append(render_to_string('excercises/checked_exercises/correct.html',{"content":content.item.correct_answer}))
                else:
                    checked_exercise.append(content.item.correct_answer)
            checked_answers.append(checked_exercise)
        correct_ratio = (len(correct_items)/exercise_set.number_of_points)*100
        context = {'checked_answers': checked_answers,"correct_ratio":correct_ratio}
        return render(request,'excercises/excercise_set_check.html',context)

class ExerciseDeleteView(View):
    def post(self, request, set_id, exercise_id):
        exercise = get_object_or_404(Exercise, pk=exercise_id)
        exercise.delete()
        return redirect('excercise_set_edit_view', set_id=set_id)