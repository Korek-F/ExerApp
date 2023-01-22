from django.shortcuts import render
from django.views.generic import View
from excercises.models import ExerciseSet
from .models import Category
from django.shortcuts import get_object_or_404

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

class AllCategoriesView(View):
    def get(self,request):
        categories = Category.objects.all()
        context = {"categories":categories}
        return render(request, "categories/all_categories.html", context)

class CategoryDetailView(View):
    def get(self, request, name):
        category = get_object_or_404(Category, name=name)
        context = {"category":category}
        exercises_sets = category.exerciseset_set.all()
        context = {"category":category,'exercises_sets':exercises_sets}
        return render(request, "categories/category_detail.html", context)