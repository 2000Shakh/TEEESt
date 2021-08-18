from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserFrom

@login_required(login_url="login_page")
def home_page(request):
    return render(request, 'loginapp/homepage.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home_page')
            else:
                messages.info(request, "ERORR")

        context = {}

    return render(request, 'loginapp/index.html', context)


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    else:
        form = CreateUserFrom
        if request.method == "POST":
            form = CreateUserFrom(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                return redirect('login_page')

        context = {'form': form}

    return render(request, 'loginapp/index.html', context)


def logout_user(request):
    logout(request)
    return redirect('login_page')
