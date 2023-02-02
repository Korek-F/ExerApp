from django.urls import path
from . import views
urlpatterns = [
    path('', views.AllExercisesSets.as_view(), name="exercises"),

    path('exercise-set/<int:set_id>/edit/', views.ExerciseSetEditView.as_view(), name="excercise_set_edit_view"),
    path('exercise-set/<int:set_id>/learn/', views.ExerciseSetLearnView.as_view(), name="excercise_set_learn_view"),
    
    path('exercise-set/<int:set_id>/check/', 
    views.ExerciseSetCheckView.as_view(), name="excercise_set_check_view"),

    path('exercise-set/<int:set_id>/exercise-delete/', 
    views.ExerciseDeleteView.as_view(), name="excercise_delete_view"),

    path('exercise-set/create/', 
    views.ExerciseSetCreationView.as_view(), name="excercise_set_create_view"),

    path('search/', views.SearchExercisesSetsView.as_view(), name="search_exercises_sets"),

    path('settings/<int:pk>/change-set-status/', views.change_set_status, name="change_set_status")
]
