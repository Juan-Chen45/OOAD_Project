from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf

from user.models import ExtendUser
from game.models import Game
from django.contrib.auth.models import User
from user.forms import UserModifyForm
from django.urls import reverse


# Create your views here.

def user_home(request):
    context = {}
    context['user'] = request.user
    context['extendUser'] = get_object_or_404(ExtendUser, user=user)
    context['games'] = context['extendUser'].game.all()

    return render(request, 'user_home.html', context)


def modify_user(request):
    user = request.user
    extend = get_object_or_404(ExtendUser, user=user)
    context = {}
    context.update(csrf(request))
    if request.method == "POST":
        reg_form = UserModifyForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            user.username = reg_form.cleaned_data["name"]
            extend.avatar = reg_form.cleaned_data['avatar']
            extend.introduction = request.POST.get('introduction', extend.introduction)
            user.save()
            extend.save()
            # redirect 去的地址要改
            return redirect(request.GET.get("from", reverse("home")))
    else:
        # 是 get
        reg_form = UserModifyForm()
    context["user"] = user
    context["extend"] = extend
    context["form"] = reg_form
    return render(request, "modify_user.html", context)
