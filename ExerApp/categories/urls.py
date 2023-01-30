from django.urls import path
from . import views
urlpatterns = [
    path('delete/<int:set_id>/', views.delete_category_from_set, name="delete_cat_from_set"),
    path('add/<int:set_id>/', views.add_category_to_set, name="add_cat_to_set"),
    path('all/', views.AllCategoriesView.as_view(), name="all_categories"),
    path('details/<str:name>/', views.CategoryDetailView.as_view(), name="category_detail"),
    path('search/', views.SearchCategoriesView.as_view(), name="search_categories"),
]
