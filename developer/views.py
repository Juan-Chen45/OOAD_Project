from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf

from .models import Developer
from game.models import Game
from django.contrib.auth.models import User
from developer.forms import UserModifyForm


def developer_home(request):
    user = request.user
    context = {'user': user}
    context['developer'] = Developer.objects.get(user=context['user'])
    return render(request, 'developer_home.html', context)


# user 看 developer
def developer_message(request, name):
    user = User.objects.get(username=name)
    context = {}
    context['developer'] = Developer.objects.get(user=user)
    gamelist = Game.objects.filter(author=context['developer'])
    context['games'] = gamelist

    return render(request, 'developer_message.html', context)


# developer 看余额,改除了password的信息
def modify_developer_message(request):
    context = {}
    context.update(csrf(request))
    user = request.user
    developer = Developer.objects.get(user=user)
    context['user'] = user
    context['developer'] = developer
    if request.method == "POST":
        reg_form = UserModifyForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            user.username = reg_form.cleaned_data["name"]
            developer.avatar = request.FILES.get('avatar', developer.avatar)
            developer.introduction = reg_form.cleaned_data["introduction"]
            user.save()
            developer.save()
            # redirect 去的地址要改
            return redirect("developer home")
    else:
        # 是 get
        reg_form = UserModifyForm()
    context["form"] = reg_form
    return render(request, "modify_developer_message.html", context)


def game_select(request):
    user = request.user
    developer = Developer.objects.get(user=user)
    game_list = Game.objects.filter(author=developer).all()
    context = {}
    context['user'] = user
    context['developer'] = developer
    context['game_list'] = game_list
    return render(request, "game_select.html", context)
