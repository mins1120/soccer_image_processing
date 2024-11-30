from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUp_Form as SignUpForm
from django.contrib.auth.decorators import login_required

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.is_valid())
        print(form.errors)  # 폼 에러 출력
        if form.is_valid():
            user = form.save()
            return redirect('home') 
    else:
        form = SignUpForm() 
    return render(request, 'user/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')