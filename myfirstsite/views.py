from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from game.models import Game
from developer.models import Developer
from read_statistic.utils import get_7days_data, get_today_hot_data
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User, AnonymousUser
from user.models import ExtendUser


def homepage(request):
    all_games = Game.objects.all()
    ct = ContentType.objects.get_for_model(Game)
    data, days = get_7days_data(ct)
    today_hot_data = get_today_hot_data(ct)
    user = request.user
    context = {'date': data, 'days': days, 'today_hot_data': today_hot_data, 'games': all_games}

    # if(hasattr(user,"developer")):
    #     login(request, user)
    # elif(hasattr(user,"extenduser")):
    #     login(request, user)

    return render(request, "home.html", context)

def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            # 由此可以让developer直接登录到自己的界面
            # if(hasattr(user,"developer")):
            #     login(request, user)
            #     return redirect("/developer/")
            # elif(hasattr(user,"extenduser")):
            #     login(request, user)
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
            if(not reg_form.cleaned_data["ifDeveloper"]):
                extendUser = ExtendUser(user=user)
            else:
                extendUser = Developer(user = user)
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
