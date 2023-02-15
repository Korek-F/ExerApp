from django.urls import path
from . import views
urlpatterns = [
    path('exam/<int:id>/create/', views.CreateExamView.as_view(), name="create_exam"),

    path('exam/<slug:slug>/', views.StartExamView.as_view(), name="exam"),

    path('session/<slug:slug>/', views.SessionView.as_view(), name="session"),

    path('session/<slug:slug>/results/', views.SessionResultsView.as_view(), name="session_results"),

    path('exam-list/', views.ExamListView.as_view(), name="exam_list"),

    path('exam/<slug:slug>/owner/', views.ExamOwnerView.as_view(), name="exam_owner_view"),

    path('session/<slug:slug>/details/', views.SessionDetailView.as_view(), name="session_detail_view"),

    path('search/exam/', views.SearchExamsView.as_view(), name="exam_search"),
]
