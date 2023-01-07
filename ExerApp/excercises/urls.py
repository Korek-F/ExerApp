from django.urls import path
from . import views
urlpatterns = [
    path('', views.mainpage, name="mainpage"),
    path('exercise-set/<int:set_id>/', views.ExerciseSetDetailView.as_view(), name="excercise_set_detail_view"),
    path('exercise-set/<int:set_id>/edit/', views.ExerciseSetEditView.as_view(), name="excercise_set_edit_view"),
    path('exercise-set/<int:set_id>/learn/', views.ExerciseSetLearnView.as_view(), name="excercise_set_learn_view"),
    
    path('exercise-set/<int:set_id>/check/', 
    views.ExerciseSetCheckView.as_view(), name="excercise_set_check_view"),
]
