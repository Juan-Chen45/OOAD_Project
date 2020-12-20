from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from game.models import Game

from read_statistic.utils import get_7days_data, get_today_hot_data
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from user.models import ExtendUser


def homepage(request):
    ct = ContentType.objects.get_for_model(Game)
    data, days = get_7days_data(ct)
    today_hot_data = get_today_hot_data(ct)

    # 本地代码这里就不加缓存了，懒得了，后续可以加上

    context = {'date': data, 'days': days, 'today_hot_data': today_hot_data}
    return render(request, "home.html", context)


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        login_form = LoginForm()
    context = {"login_form": login_form}
    return render(request, "login.html", context)


def reguser(request):
    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            username = reg_form.cleaned_data["username"]
            email = reg_form.cleaned_data["email"]
            password = reg_form.cleaned_data["password_again"]
            user = User.objects.create_user(username, email, password)
            extendUser = ExtendUser.objects.create(user=user)
            user.save()
            extendUser.save()
            login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        reg_form = RegisterForm()
    context = {"reg_form": reg_form}
    return render(request, "register.html", context)


def user_logout(request):
    logout(request)
    return redirect(reverse("home"))
