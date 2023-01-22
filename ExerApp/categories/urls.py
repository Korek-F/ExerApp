from django.urls import path
from . import views
urlpatterns = [
    path('delete/<int:set_id>/', views.delete_category_from_set, name="delete_cat_from_set"),
    path('add/<int:set_id>/', views.add_category_to_set, name="add_cat_to_set"),
]
