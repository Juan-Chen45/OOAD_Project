from django.shortcuts import render, get_object_or_404, redirect
from .models import Developer, Game, GameType, GameShow, Version, DLC


def home(request, developer_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    return render(request, 'developer/developer_home.html', context)


def developer_games(request, developer_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    context['games'] = Game.objects.filter(developer=context['developer'])
    return render(request, 'developer/developer_games.html', context)


def versions_dlcs(request, developer_pk, game_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    context['game'] = get_object_or_404(Game, pk=game_pk)
    context['versions'] = Version.objects.filter(game=context['game'])
    context['dlcs'] = DLC.objects.filter(game=context['game'])
    return render(request, 'developer/versions_dlcs.html', context)


def change_info(request, developer_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    return render(request, 'developer/developer_change_info.html', context)


def change_info_submit(request):
    developer = Developer.objects.get(pk=request.POST.get('developer_pk'))
    developer.name = request.POST.get('name', '')
    developer.avatar = request.FILES.get('avatar', developer.avatar)
    developer.introduction = request.POST.get('introduction', '')
    # print(developer.avatar.url)
    # print(developer.name)
    developer.save()

    return redirect(str(developer.pk) + '/change_info')


#user 看 developer
def developer_message(request,developer_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    gamelist=Game.objects.filter(developer=context['developer'])
    context['games']=gamelist
    return render(request, 'developer/developer_message.html', context)
    
#看 game,改game信息
#添加宣传图
def modify_game_message(request,developer_pk,game_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    context['games']=get_object_or_404(Game, pk=game_pk)
    return render(request, 'developer/modify_game_message.html', context)

def modify_game_message_submit(request):
    game=Game.objects.get(request.POST.get(name='game'))
    game.name = request.POST.get('name', '')
    game.avatar = request.FILES.get('inputimage', game.avatar)
    game.introduction = request.POST.get('introduction', '')
    game.price=request.POST.get("price",game.price)
    game.file=request.FILES.get("inputfile",game.file)
    game.announce_date=request.POST.get("announce_date",game.announce_date)
    game.release_date=request.POST.get("release_date",game.release_date)
    
    tag_list = request.POST.getlist("tag")
    for tag in tag_list:
        game.type.add(tag)
    game.save()
    return redirect(str(game.pk) + '/change_info')

#添加game
def add_game(request,developer_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    return render(request,'developer/add_game.html',context)

def add_game_submit(request):
    game=Game()
    game.name = request.POST.get('name', '')
    game.avatar = request.FILES.get('inputimage', game.avatar)
    game.introduction = request.POST.get('introduction', '')
    game.price=request.POST.get("price",game.price)
    game.file=request.FILES.get("inputfile",game.file)
    game.announce_date=request.POST.get("announce_date",game.announce_date)
    game.release_date=request.POST.get("release_date",game.release_date)
    game.developer=Developer.objects.get(pk=request.POST.get('developer_pk'))
    tag_list = request.POST.getlist("tag")
    for tag in tag_list:
        game.type.add(tag)
    game.save()
    return redirect(str(game.pk) + '/change_info')

#添加折扣
def set_discount(request,developer_pk):
    context = {}
    context['developer'] = get_object_or_404(Developer, pk=developer_pk)
    gamelist=Game.objects.filter(developer=context['developer'])
    context['games']=gamelist
    return render(request, 'developer/set_discount.html', context)

def set_discount_submit(request):
    game=Game.objects.get(request.POST.get(name='game'))
    discount=Discount()
    discount.status='GAME'
    discount.game=game
    discount.from_date=request.POST.get("from_date",'')
    discount.to_date=request.POST.get("to_date",'')
    discount.price=request.POST.get("price",0)
    discount.save()
    return redirect(str(discount.pk) + '/change_info')