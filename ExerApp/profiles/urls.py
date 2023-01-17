from django.urls import path
from . import views
urlpatterns = [
    path('<int:pk>/', views.ProfileDetailView.as_view(), name="profile_detail"),
]
