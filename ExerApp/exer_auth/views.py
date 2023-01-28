from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



class LoginView(View):
    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            messages.error(request, "You are arleady logged in!" )
            return redirect('exercises')
        context["form"]=AuthenticationForm
        return render(request,'exer_auth/login.html' ,context)
    
    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Successfully logged in!" )
            return redirect('exercises')
        context = {}
        context["form"]=form
        return render(request,'exer_auth/login.html' ,context)


def logout_view(request):
    if request.method=="POST":
        logout(request)
        messages.success(request, "Successfully logged out!" )
        return redirect('login')
    return render(request, 'exer_auth/logout.html')