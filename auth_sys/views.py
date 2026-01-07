from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import auth_sys.models as models


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("blog:index")
        else:
            messages.error(request, "Неправильний пароль чи логін!")
            return render(request, "auth_sys/login.html")
    elif request.method == "GET":
        return render(request, "auth_sys/login.html")

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        if not username or not email or not password:
            messages.error(request, "Юзернейм, почта та пароль обов'язкові!")
            return render(request, "auth_sys/register.html")
        if password != password_confirm:
            messages.error(request, "Ви не змогли повторити ваш пароль правильно!")
            return render(request, "auth_sys/register.html")

        first_name = request.POST.get("first_name")
        if first_name == "": first_name = None
        last_name = request.POST.get("last_name")
        if last_name == "": last_name = None
        birth_date = request.POST.get("birth_date")
        if birth_date == "": birth_date = None

        user = models.MyUser.objects.create_user(username=username, email=email, password=password,
                                                 first_name=first_name, last_name=last_name, birth_date=birth_date)
        login(request, user)

        return redirect("blog:index")

    elif request.method == "GET":
        return render(request, "auth_sys/register.html")

@login_required
def logout_user(request):
    logout(request)
    return redirect("blog:index")
