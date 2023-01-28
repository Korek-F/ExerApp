from django.shortcuts import render
from django.views.generic import View
from excercises.models import ExerciseSet
from .models import Category
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from .forms import CreateCategoryForm

def delete_category_from_set(request, set_id):
    if request.method == 'POST':
        exercise_set = get_object_or_404(ExerciseSet, id=set_id)

        category = get_object_or_404(Category, id=request.POST.get("delete_id"))
        exercise_set.categories.remove(category)
        category.popularity -= 1
        category.save()
        
        messages.success(request,f"Removed from category {category.name}")

        new_form =  CreateCategoryForm(initial={"set_id":set_id})
        context = {"exercise_set":exercise_set,"form":new_form}
        
        return render(request, 'categories/partials/add_category_form.html',context)

def add_category_to_set(request, set_id):
    if request.method == 'POST':
        exercise_set = get_object_or_404(ExerciseSet, id=set_id)
        
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Added to category {obj.name}" )
            form =  CreateCategoryForm(initial={"set_id":set_id})
        context = {"exercise_set":exercise_set,"form":form}
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