from django.shortcuts import render, get_object_or_404
from django.views import  View
from django.views.generic import ListView
from .models import ExerciseSet,Exercise
from django.shortcuts import redirect
from .forms import ExerciseSetCreationForm, ExerciseSetPublicStatus
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from categories.forms import CreateCategoryForm
from .utils import create_content, render_checked_exercise, check_ansewers
from django.db.models import Q 


class AllExercisesSets(View):
    def get(self, request, *args, **kwargs):
        exercises_sets = ExerciseSet.objects.all().filter(is_public=True)
        context = {'exercises_sets': exercises_sets}
        return render(request, 'excercises/all_excercises_sets_page.html', context)


class ExerciseSetEditView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        form = CreateCategoryForm(initial={"set_id":kwargs['set_id']})
        context = {'exercise_set': exercise_set, 
        'count':len(exercise_set.exercise_set.all()),
        'form':form,
        'form2':ExerciseSetPublicStatus(instance=exercise_set)}
        if not request.user == exercise_set.owner:
            return redirect(reverse("excercise_set_learn_view", kwargs={"set_id":kwargs['set_id']}))

        return render(request,'excercises/excercise_set_edit.html',context)
    
    def post(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        context = {'exercise_set': exercise_set}
        if not request.user == exercise_set.owner:
            return redirect(reverse("excercise_set_learn_view", kwargs={"set_id":kwargs['set_id']}))

        current_ex = Exercise.objects.create(exercise_set=exercise_set)

        [create_content(current_ex, i, request) for i in request.POST if i.startswith("content")]
           
        messages.success(request, "Exercise added!")
        return render(request, 'excercises/partials/exercise_edit_form.html', context)

class ExerciseSetLearnView(View):
    def get(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        context = {'exercise_set': exercise_set}
        return render(request,'excercises/excercise_set_learn.html',context)

class ExerciseSetCheckView(View):
    def post(self, request, *args, **kwargs):
        exercise_set = get_object_or_404(ExerciseSet, pk=kwargs['set_id'])
        
        #Checking answers
        correct_items, wrong_items = check_ansewers(request)
        #rendering answers
        checked_answers = []
        for exercise in exercise_set.exercise_set.all():
            checked_exercise = render_checked_exercise(exercise, correct_items, wrong_items)
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
            messages.success(request, "Exercise deleted!")
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
            context["object"] = obj
            messages.success(request, "Created succesfully!")
            return render(request, 'excercises/partials/exercise_set_create_succesful.html', context)
            
        return render(request, 'excercises/exercise_set_create.html',context)


class SearchExercisesSetsView(ListView):
    model = ExerciseSet
    template_name = "excercises/partials/search_sets.html"


    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = ExerciseSet.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
            | Q(categories__name__icontains=query)
        )
        return object_list
    
def change_set_status(request, pk):
    if request.method =="POST":
        print(pk)
        instance = get_object_or_404(ExerciseSet, id=pk)
        form = ExerciseSetPublicStatus(data=request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Edited succesfully!")
        context = {}
        context["form2"] = form
        context["exercise_set"]=instance
        return render(request, 'excercises/partials/change_set_status.html',context)
        