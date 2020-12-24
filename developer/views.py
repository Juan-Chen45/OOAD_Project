from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.urls import reverse

from .models import Developer
from game.models import Game, DLC, Version
from django.contrib.auth.models import User
from developer.forms import UserModifyForm


def developer_home(request):
    user = request.user
    context = {'user': user}
    context['developer'] = get_object_or_404(Developer, user=request.user)
    return render(request, 'developer_home.html', context)


# # user 看 developer
# def developer_message(request, name):
#     user = User.objects.get(username=name)
#     context = {}
#     context['developer'] = get_object_or_404(Developer, user=request.user)
#     gamelist = Game.objects.filter(author=context['developer'])
#     context['games'] = gamelist
#     return render(request, 'developer_message.html', context)


# developer 看余额,改除了password的信息
def modify_developer_message(request):
    # context = {}
    # context.update(csrf(request))
    # user = request.user
    # developer = get_object_or_404(Developer, user=request.user)
    # context['user'] = user
    # context['developer'] = developer
    # if request.method == "POST":
    #     reg_form = UserModifyForm(request.POST, request.FILES)
    #     # 验证过了，说明用户验证也成功了
    #     if reg_form.is_valid():
    #         user.username = reg_form.cleaned_data["name"]
    #         developer.avatar = reg_form.cleaned_data['avatar']
    #         developer.introduction = reg_form.cleaned_data["introduction"]
    #         user.save()
    #         developer.save()
    #         # redirect 去的地址要改
    #         return redirect("developer home")
    # else:
    #     # 是 get
    #     reg_form = UserModifyForm()
    # context["form"] = reg_form
    # return render(request, "modify_developer_message.html", context)
    user = request.user
    developer = get_object_or_404(Developer, user=user)
    context = {}
    context.update(csrf(request))
    if request.method == "POST":
        # 当有数据上传时，要把request.FILES传入
        # 同时前端要加enctype="multipart/form-data"

        modify_form = UserModifyForm(request.POST,request.FILES)
        # 验证过了，说明用户验证也成功了
        if modify_form.is_valid():
            user.username = modify_form.cleaned_data["name"]
            developer.introduction =modify_form.cleaned_data["introduction"]
            if(modify_form.cleaned_data['avatar'] is not None):
                developer.avatar = modify_form.cleaned_data['avatar']
            user.save()
            developer.save()
            # redirect 去的地址要改
            return redirect(reverse("developer home"))
    else:
        # 是 get
        initial = {"name": user.username, "introduction": developer.introduction,"avatar":developer.avatar}
        modify_form = UserModifyForm(initial=initial)
    context["user"] = user
    context["developer"] = developer
    context["form"] = modify_form
    return render(request, "modify_developer_message.html", context)

def game_select(request):
    user = request.user
    developer = get_object_or_404(Developer,user=request.user)
    game_list = Game.objects.filter(author=developer).all()
    context = {}
    context['user'] = user
    context['developer'] = developer
    context['game_list'] = game_list
    return render(request, "game_select.html", context)


def dlc_select(request):
    user = request.user
    developer = get_object_or_404(Developer,user=request.user)
    game_list = Game.objects.filter(author=developer).all()
    context = {}
    dlc_list = []
    branch_list = []
    for game in game_list:
        dlcs = DLC.objects.filter(game=game)
        branchs = Version.objects.filter(game=game)
        for dlc in dlcs:
            dlc_list.append(dlc)
        for branch in branchs:
            branch_list.append(branch)
        context['user'] = user
        context['developer'] = developer
        context['dlc_list'] = dlc_list
        context['brach_list'] = branch_list
    return render(request, "dlc_select.html", context)
