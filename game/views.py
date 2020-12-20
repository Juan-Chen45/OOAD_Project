from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

from comment.forms import CommentForm
from comment.models import Comment
from game.forms import GameRegisterForm
from developer.models import Developer
from read_statistic.utils import cookie_read
from .models import GameType, Game, Version, DLC


# Create your views here.

def game_list(request):
    all_games = Game.objects.all()
    context = get_game_common(request, all_games)
    return render(request, "game_list.html", context)


def game_detail(request, game_id):
    currgame = get_object_or_404(Game, pk=game_id)

    # 获得这个game对应的comment

    game_content_type = ContentType.objects.get_for_model(currgame)
    comments = Comment.objects.filter(content_type=game_content_type, object_id=game_id)

    cookie_key = cookie_read(request, currgame)

    context = {}
    context["game"] = currgame
    context["previous_game"] = Game.objects.filter(create_time__gt=currgame.create_time).last()
    context["next_game"] = Game.objects.filter(create_time__lt=currgame.create_time).first()
    context["dlcs"] = DLC.objects.filter(game=currgame)
    context["versions"] = Version.objects.filter(game=currgame)
    context["comments"] = comments

    # 用来初始化CommentForm里面的一些参数
    data = {}
    data["content_type"] = game_content_type.model
    data["object_id"] = game_id
    context["comment_form"] = CommentForm(initial=data)

    response = render(request, "game_detail.html", context)
    response.set_cookie(cookie_key, 'true')

    return response


def get_game_name(request, game_type_name):
    type = get_object_or_404(GameType, type_name=game_type_name)
    all_games = Game.objects.filter(game_type=type)
    context = get_game_common(request, all_games)
    context["name"] = game_type_name
    return render(request, "game_type_list.html", context)


def game_with_date(request, year, month):
    all_games = Game.objects.filter(create_time__year=year, create_time__month=month)
    context = get_game_common(request, all_games)
    context["curr_time"] = "%s 年 %s 月" % (year, month)
    return render(request, "game_with_date.html", context)


def get_game_common(request, all_games):
    page_num = request.GET.get("page", 1)  # 获取url页面的get参数，默认返回第一页
    paginator = Paginator(all_games, settings.GAME_PER_PAGE)  # 每7个游戏一页
    current_page = paginator.get_page(
        page_num)  # 这个方法很好，不要用paginator.page(1)，因为这个能处理超出范围，字符串数字转换等等的问题，毕竟你get获得的参数是字符串嘛，用page函数还要转成int，还可能是abc呢怎么办！
    # 只要当前页面的前两页和后两页
    page_range = [page for page in range((current_page.number - 2), (current_page.number + 3)) if
                  0 < page <= paginator.num_pages]
    # 实现省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    # 实现第一页与最后一页的显示
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context["games"] = current_page
    context["types"] = GameType.objects.annotate(game_count=Count("game"))
    context["page_range"] = page_range
    context["game_date"] = Game.objects.dates("create_time", "month", order="DESC")
    return context


# version 的介绍页面
def version_detail(request, version_id):
    currversion = get_object_or_404(Version, pk=version_id)

    # 获得这个game对应的comment

    # game_content_type = ContentType.objects.get_for_model(currgame)
    # comments = Comment.objects.filter(content_type=game_content_type, object_id=game_id)
    cookie_key = cookie_read(request, currversion)

    context = {}
    context["game"] = currversion
    context["previous_game"] = Version.objects.filter(game=currversion.game).filter(
        create_time__gt=currversion.create_time).last()
    context["next_game"] = Version.objects.filter(game=currversion.game).filter(
        create_time__lt=currversion.create_time).first()
    # context["comments"] = comments

    # 用来初始化CommentForm里面的一些参数
    # data = {}
    # data["content_type"] = game_content_type.model
    # data["object_id"] = game_id
    # context["comment_form"] = CommentForm(initial=data)

    response = render(request, "version_detail.html", context)
    response.set_cookie(cookie_key, 'true')

    return response


# dlc的介绍页面
def dlc_detail(request, dlc_id):
    currversion = get_object_or_404(DLC, pk=dlc_id)

    # 获得这个game对应的comment

    # game_content_type = ContentType.objects.get_for_model(currgame)
    # comments = Comment.objects.filter(content_type=game_content_type, object_id=game_id)
    cookie_key = cookie_read(request, currversion)

    context = {}
    context["game"] = currversion
    context["previous_game"] = DLC.objects.filter(game=currversion.game).filter(
        create_time__gt=currversion.create_time).last()
    context["next_game"] = DLC.objects.filter(game=currversion.game).filter(
        create_time__lt=currversion.create_time).first()
    # context["comments"] = comments

    # 用来初始化CommentForm里面的一些参数
    # data = {}
    # data["content_type"] = game_content_type.model
    # data["object_id"] = game_id
    # context["comment_form"] = CommentForm(initial=data)

    response = render(request, "dlc_detail.html", context)
    response.set_cookie(cookie_key, 'true')

    return response


def regist_game(request):
    if request.method == "POST":
        reg_form = GameRegisterForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            name = reg_form.cleaned_data["name"]
            game_type = request.POST.get('game_type', None)
            introduction = request.POST.get('introduction', '')
            author = Developer.objects.filter(user=request.user)
            price = reg_form.cleaned_data["price"]
            avatar = reg_form.cleaned_data["avatar"]
            game = Game.objects.create(name=name, game_type=game_type, introduction=introduction, author=author,
                                       price=price, avatar=avatar)
            game.save()
            # redirect 去的地址要改
            return redirect(request.GET.get("from", reverse("home")))
        else:
            context = {}
            context["form"] = reg_form
            context["types"] = GameType.objects.filter()
            context["clear_errors"] = reg_form.errors.get("__all__")
            return render(request, "add_game.html", context)
    else:
        # 是 get
        reg_form = GameRegisterForm(request.POST)
        context = {}
        context["form"] = reg_form
        context["types"] = GameType.objects.filter()
        return render(request, "add_game.html", context)


def modify_game(request, game_name):
    if request.method == "POST":
        reg_form = GameRegisterForm(request.POST)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            game = Game.objects.filter(name=game_name)
            game.name = reg_form.cleaned_data["name"]
            game.game_type = request.POST.get('game_type', game.game_type)
            game.introduction = request.POST.get('introduction', game.introduction)
            game.author = Developer.objects.filter(user=request.user)
            game.price = reg_form.cleaned_data["price"]
            game.avatar = reg_form.cleaned_data["avatar"]
            game.save()
            # redirect 去的地址要改
            return redirect(request.GET.get("from", reverse("home")))
        else:
            context = {}
            context["game"] = Game.objects.filter(name=game_name)
            context["form"] = reg_form
            context["types"] = GameType.objects.filter()
            context["clear_errors"] = reg_form.errors.get("__all__")
            return render(request, "modify_game.html", context)
    else:
        # 是 get
        reg_form = GameRegisterForm(request.POST)
        context = {}
        context["game"] = Game.objects.filter(name=game_name)
        context["form"] = reg_form
        context["types"] = GameType.objects.filter()
        return render(request, "modify_game.html", context)
