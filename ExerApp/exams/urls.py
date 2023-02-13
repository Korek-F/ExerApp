from django.urls import path
from . import views
urlpatterns = [
    path('exam/<slug:slug>/', views.StartExamView.as_view(), name="exam"),
    path('session/<slug:slug>/', views.SessionView.as_view(), name="session"),
    path('session/<slug:slug>/results/', views.SessionResultsView.as_view(), name="session_results"),
]
