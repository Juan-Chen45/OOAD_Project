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
    gamelist = Game.objects.filter(developer=context['developer'])
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
            developer.introduction = request.POST.get('introduction', developer.introduction)
            user.save()
            developer.save()
            # redirect 去的地址要改
            return redirect("developer home")
    else:
        # 是 get
        reg_form = UserModifyForm()
    context["form"] = reg_form
    return render(request, "modify_developer_message.html", context)

# 加入developer看自己持有的游戏 修改游戏
