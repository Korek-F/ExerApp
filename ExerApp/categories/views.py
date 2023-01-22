from django.shortcuts import render
from django.views.generic import View
from excercises.models import ExerciseSet
from .models import Category
from django.shortcuts import get_object_or_404
# Create your views here.
def delete_category_from_set(request, set_id):
    if request.method == 'POST':
        exercise_set = get_object_or_404(ExerciseSet, id=set_id)
        context = {"exercise_set":exercise_set}
        category = get_object_or_404(Category, id=request.POST.get("delete_id"))
        exercise_set.categories.remove(category)
        return render(request, 'categories/partials/add_category_form.html',context)

def add_category_to_set(request, set_id):
    if request.method == 'POST':
        exercise_set = get_object_or_404(ExerciseSet, id=set_id)
        context = {"exercise_set":exercise_set}
        cat_name = request.POST.get("cat_name").upper()
        if Category.objects.filter(name=cat_name).exists():
            cat = Category.objects.get(name=cat_name)
        else:
            cat = Category(name=cat_name)
        cat.save()

        exercise_set.categories.add(cat)
        
        return render(request, 'categories/partials/add_category_form.html',context)