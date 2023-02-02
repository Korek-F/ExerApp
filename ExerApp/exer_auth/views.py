from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserCreationForm




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

class SignUpView(View):
    def get(self,request):
        if request.user.is_authenticated:
            messages.error(request, "You are arleady logged in!" )
            return redirect('exercises')
        context = {}
        context['form'] = UserCreationForm()
        return render(request, 'exer_auth/signup.html',context)

    def post(self, request):
        print(request.POST)
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully signed up!" )
            return redirect('login')
        context = {}
        context["form"]=form
        return render(request, 'exer_auth/signup.html',context)


def logout_view(request):
    if request.method=="POST":
        logout(request)
        messages.success(request, "Successfully logged out!" )
        return redirect('login')
    return render(request, 'exer_auth/logout.html')