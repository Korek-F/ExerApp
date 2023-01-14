from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import ExerciseSet, BlankText,Exercise, Text, Content, Hint, ABCD
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from .forms import ExerciseSetCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class AllExercisesSets(View):
    def get(self, request, *args, **kwargs):
        exercises_sets = ExerciseSet.objects.all()
        context = {'exercises_sets': exercises_sets}
        return render(request, 'excercises/all_excercises_sets_page.html', context)






class ExerciseSetEditView(View):
    def get(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        context = {'exercise_set': exercise_set,  
        'count':len(exercise_set.exercise_set.all())}
        return render(request,'excercises/excercise_set_edit.html',context)
    
    def post(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        context = {'exercise_set': exercise_set}
        
        current_ex = Exercise.objects.create(exercise_set=exercise_set)
        for i in request.POST:
            if i.startswith("content"):
                content_type = i.split("-")[1]
                if content_type=="Text":
                    content_item = Text.objects.create(content=request.POST[i])
                    cc = ContentType.objects.get_for_model(Text)
                elif content_type=="Blank":
                    content_item = BlankText.objects.create(correct=request.POST[i])
                    cc = ContentType.objects.get_for_model(BlankText)
                elif content_type=="ABCD":
                    content_item = ABCD.objects.create(answers=request.POST[i])
                    cc = ContentType.objects.get_for_model(ABCD)
                else:
                    content_item = Hint.objects.create(content=request.POST[i])
                    cc = ContentType.objects.get_for_model(Hint)

                Content.objects.create(exercise=current_ex, content_type=cc,object_id=content_item.id)
        
        return render(request, 'excercises/partials/exercise_edit_form.html', context)

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
            if i.startswith('answer_blank') or i.startswith('answer_abcd'):
                obj_id = int(i.split("_")[2])
                obj = get_object_or_404(Content, pk=obj_id).item
                answer = request.POST[i]
                if obj.is_correct(answer):
                    correct_items.append(obj)
                else:
                    wrong_items[obj]=answer

        checked_answers = []
        for exercise in exercise_set.exercise_set.all():
            checked_exercise = []
            for content in exercise.content_set.all():

                if content.item.content_type not in ['text', 'hint']:
                    if not content.item in correct_items:
                        answer = wrong_items[content.item]
                        if answer == '': answer="___" 
                        checked_exercise.append(render_to_string('excercises/checked_exercises/wrong.html',{"correct":content.item.correct_answer,
                        "answer":answer}
                         ))

                    else:
                        checked_exercise.append(render_to_string('excercises/checked_exercises/correct.html',{"content":content.item.correct_answer}))
                else:
                    checked_exercise.append(content.item.correct_answer)
            checked_answers.append(checked_exercise)

        correct_ratio = (len(correct_items)/exercise_set.number_of_points)*100
        context = {
            'exercise_set':exercise_set,
            'checked_answers': checked_answers,
            "correct_ratio":correct_ratio}

        return render(request,'excercises/excercise_set_check.html',context)

class ExerciseDeleteView(View):
    def post(self, request, set_id):
        exercise_set = get_object_or_404(ExerciseSet, pk=set_id)
        context = {'exercise_set': exercise_set}
        if request.POST.get("delete_id"):
            get_object_or_404(Exercise, pk=request.POST.get("delete_id")).delete()

        return render(request, 'excercises/partials/exercise_edit_form.html', context)


class ExerciseSetCreationView(LoginRequiredMixin,View):
    
    def get(self, request):
        form = ExerciseSetCreationForm()
        context = {'form':form}
        return render(request, 'excercises/exercise_set_create.html',context)
    
    def post(self, request):
        form = ExerciseSetCreationForm(request.POST or None)
        context={}
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            context["message"]="Created succesfully!"
            context["object"] = obj
            return render(request, 'excercises/partials/exercise_set_create_succesful.html', context)
            
        return render(request, 'excercises/exercise_set_create.html',context)