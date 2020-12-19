from django.shortcuts import get_object_or_404, render
from .models import GameType, Game
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from read_statistic.utils import cookie_read
from django.contrib.contenttypes.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm


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
                  page > 0 and page <= paginator.num_pages]
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
