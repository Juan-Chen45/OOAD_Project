from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from game.models import Game

from read_statistic.utils import get_7days_data, get_today_hot_data
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect
from django.urls import reverse
from .forms import LoginForm,RegisterForm
from django.contrib.auth.models import User


def homepage(request):
    ct = ContentType.objects.get_for_model(Game)
    data, days = get_7days_data(ct)
    today_hot_data = get_today_hot_data(ct)
    # 本地代码这里就不加缓存了，懒得了，后续可以加上
    context = {}
    context['date'] = data
    context['days'] = days
    context['today_hot_data'] = today_hot_data
    return render(request,"home.html", context)


def user_login(request):
    # if request.method == "POST":
    #     username = request.POST.get("username", "")
    #     password = request.POST.get("password", "")
    #     user = authenticate(request, username=username, password=password)
    #     # 这里获得了request是从哪来的的消息，这样就可以直接redirect回原本页面。取不到就返回首页
    #     referer = request.META.get("HTTP_REFERER", reverse("home"))
    #     if user is not None:
    #         login(request, user)
    #         # Redirect to a success page.
    #         return redirect(referer)
    #     else:
    #         # Return an 'invalid login' error message.
    #         return render(request, 'error.html', {"message": "用户名或密码不正确"})
    # else:
    #     return render(request,"login.html",{})
    # ==============================================================================
    # 这部分是把用户验证放在这里,接下来我们要把用户验证放到forms表单里面
    # if request.method == "POST":
    #     login_form = LoginForm(request.POST)
    #     # 验证过了，数据比较好
    #     if login_form.is_valid():
    #         username = login_form.cleaned_data["username"]
    #         password = login_form.cleaned_data["password"]
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             # Redirect to a success page.
    #             # 返回进入login的上一个页面，默认返回home
    #             return redirect(request.GET.get("from",reverse("home")))
    #         else:
    #             # Return an 'invalid login' error message.
    #             login_form.add_error(None,"用户名或密码不正确")
    # else:
    #     login_form = LoginForm()
    #
    # context = {}
    # context["login_form"] = login_form
    # return render(request,"login.html",context)

#     ===============================================================================
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if login_form.is_valid():
            user = login_form.cleaned_data["user"]
            login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        login_form = LoginForm()
    context = {}
    context["login_form"] = login_form
    return render(request, "login.html", context)


def reguser(request):
    if request.method == "POST":
        reg_form = RegisterForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            username = reg_form.cleaned_data["username"]
            email = reg_form.cleaned_data["email"]
            password = reg_form.cleaned_data["password_again"]
            user = User.objects.create_user(username,email,password)
            user.save()
            login(request, user)
            return redirect(request.GET.get("from", reverse("home")))
    else:
        reg_form = RegisterForm()
    context = {}
    context["reg_form"] = reg_form
    return render(request, "register.html", context)

def user_logout(request):
    logout(request)
    return redirect(reverse("home"))