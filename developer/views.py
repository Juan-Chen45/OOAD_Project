from django.shortcuts import render, get_object_or_404, redirect
from .models import Developer
from game.models import Game
from django.contrib.auth.models import User


def developer_home(request):
    user = request.user
    context = {'user': user}
    context['developer'] = Developer.objects.get(user=context['user'])
    return render(request, 'developer/developer_home.html', context)


# user 看 developer
def developer_message(request, name):
    context = {'user': User.objects.get(username=name)}
    context['developer'] = Developer.objects.get(user=context['user'])
    gamelist = Game.objects.filter(developer=context['developer'])
    context['games'] = gamelist

    return render(request, 'developer/developer_message.html', context)


# developer 看余额,改除了password的信息
def modify_developer_message(request, name):
    context = {'user': User.objects.get(username=name)}
    context['developer'] = Developer.objects.get(user=context['user'])
    return render(request, 'developer/modify_developer_message.html', context)


def change_info_submit(request):
    developer = Developer.objects.get(pk=request.POST.get('developer_pk'))
    developer.user.username = request.POST.get('name', '')
    developer.avatar = request.FILES.get('avatar', developer.avatar)

    developer.introduction = request.POST.get('introduction', '')
    print(developer.avatar.url)
    print(developer.name)
    developer.save()

    return redirect(str(developer.pk) + '/change_info')
