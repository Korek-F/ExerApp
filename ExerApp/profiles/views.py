from django.shortcuts import render
from django.views.generic import DetailView
from exer_auth.models import User

class ProfileDetailView(DetailView):
    model = User
    template_name = "profiles/profile_details.html"