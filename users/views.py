import re
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.contrib.auth import login, logout

from posts.views import post_list
from users.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
# Create your views here.


def login_view(request: HttpRequest):
    form = LoginForm()
    if request.method.lower() == "post":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = User.objects.get(username=cleaned_data["username"])
            if user.check_password(cleaned_data["password"]):
                login(request, user)
                return redirect("post_list")
            else:
                form.add_error("password", "wrong password")

    return render(request, "users/login.html", context={"form": form})


def register_view(request: HttpRequest):
    form = RegisterForm()
    if request.method.lower() == "post":
        form = RegisterForm(request.POST)

        if form.is_valid():
            cleaned_data = form.cleaned_data
            form.instance.set_password(cleaned_data["password"])
            form.instance.save()
            login(request, form.instance)
            return redirect("post_list")
    return render(request, "users/register.html", context={"form": form})


def logout_view(request: HttpRequest):

    if request.method.lower() == "post":
        logout(request)

    return redirect("post_list")
