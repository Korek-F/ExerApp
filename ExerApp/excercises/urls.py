from django.urls import path
from . import views
urlpatterns = [
    path('exercises/', views.AllExercisesSets.as_view(), name="exercises"),

    path('exercise-set/<int:set_id>/edit/', views.ExerciseSetEditView.as_view(), name="excercise_set_edit_view"),
    path('exercise-set/<int:set_id>/learn/', views.ExerciseSetLearnView.as_view(), name="excercise_set_learn_view"),
    
    path('exercise-set/<int:set_id>/check/', 
    views.ExerciseSetCheckView.as_view(), name="excercise_set_check_view"),

    path('exercise-set/<int:set_id>/exercise-delete/<int:exercise_id>', 
    views.ExerciseDeleteView.as_view(), name="excercise_delete_view"),
]
