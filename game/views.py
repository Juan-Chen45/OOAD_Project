from datetime import date

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context_processors import csrf
from django.urls import reverse
from comment.forms import CommentForm
from comment.models import Comment
from user.models import ExtendUser
from game.forms import GameRegisterForm, DiscountRegisterForm, DLCRegisterForm, BranchRegisterForm
from developer.models import Developer
from read_statistic.utils import cookie_read
from .models import GameType, Game, Version, DLC, Discount


# Create your views here.

def game_list(request):
    all_games = Game.objects.all()
    context = get_game_common(request, all_games)
    return render(request, "game_list.html", context)


def game_detail(request, game_id):
    currgame = get_object_or_404(Game, pk=game_id)
    user = request.user
    context = {}
    # 此处樊顺需要注意，没有登录的用户浏览的时候是看不到purchase的
    # if(not isinstance(user,AnonymousUser)):
    #     extend = get_object_or_404(ExtendUser, user=user)
    #     purchased = False
    #     for game in extend.version.all():
    #         if game.pk == game_id:
    #             purchased = True
    #             break
    #     context["purchased"] = purchased

    # 获得这个game对应的comment

    game_content_type = ContentType.objects.get_for_model(currgame)
    comments = Comment.objects.filter(content_type=game_content_type, object_id=game_id)

    cookie_key = cookie_read(request, currgame)
    context["game"] = currgame
    context["previous_game"] = Game.objects.filter(create_time__gt=currgame.create_time).last()
    context["next_game"] = Game.objects.filter(create_time__lt=currgame.create_time).first()
    # context["dlcs"] = DLC.objects.filter(game=currgame)
    # context["versions"] = Version.objects.filter(game=currgame)
    context["comments"] = comments

    # 用来初始化CommentForm里面的一些参数
    data = {}
    data["content_type"] = game_content_type.model
    data["object_id"] = game_id
    context["comment_form"] = CommentForm(initial=data)
    context['versions'] = currgame.game_version.all()
    context['dlcs'] = currgame.dlc_version.all()
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
def version_detail(request, game_name, version_id):
    currversion = get_object_or_404(Version, pk=version_id)
    context = {}
    context["version"] = currversion
    discounts = Discount.objects.filter(game=currversion.game).all()
    flag = True
    for d in discounts:
        if d.from_date < date.today() < d.to_date:
            price = d.price
            flag = False
            break
    if flag:
        price = currversion.price
    context['price'] = price
    context["purchased"] = False
    extend = request.user.extenduser
    if extend.version.filter(pk=version_id).exists():
        context["purchased"] = True
    response = render(request, "version_detail.html", context)
    return response


# dlc的介绍页面
def dlc_detail(request, game_name, dlc_id):
    currversion = get_object_or_404(DLC, pk=dlc_id)
    context = {}
    context["dlc"] = currversion
    discounts = Discount.objects.filter(dlc=currversion).all()
    flag = True
    for d in discounts:
        if d.from_date < date.today() < d.to_date:
            price = d.price
            flag = False
            break
    if flag:
        price = currversion.price
    context['price'] = price
    context["purchased"] = False
    extend = request.user.extenduser
    if extend.dlc.filter(pk=dlc_id).exists():
        context["purchased"] = True
    response = render(request, "dlc_detail.html", context)
    return response


def regist_game(request):
    context = {}
    context.update(csrf(request))
    context['developer'] = get_object_or_404(Developer, user=request.user)
    if request.method == "POST":
        reg_form = GameRegisterForm(request.POST, request.FILES)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            name = reg_form.cleaned_data["name"]
            # 还未在html里加入这个复选框
            introduction = reg_form.cleaned_data['introduction']
            author = Developer.objects.get(user=request.user)
            typelist = reg_form.cleaned_data['type']
            avatar = reg_form.cleaned_data['avatar']
            game = Game.objects.create(name=name, introduction=introduction, author=author,
                                       avatar=avatar, game_type=typelist)
            game.save()
            # redirect 去的地址要改
            return redirect(request.GET.get("from", reverse("developer home")))
        else:

            context["form"] = reg_form
            context["types"] = GameType.objects.filter()
            # context["clear_errors"] = reg_form.errors.get("__all__")
            return render(request, "add_game.html", context)
    else:
        # 是 get
        reg_form = GameRegisterForm()
        context["form"] = reg_form
        return render(request, "add_game.html", context)


def add_dlc(request, game_name):
    context = {}
    context.update(csrf(request))
    developer = get_object_or_404(Developer, user=request.user)
    game = Game.objects.get(name=game_name)
    context['developer'] = developer
    context['game'] = game
    if request.method == "POST":
        reg_form = DLCRegisterForm(request.POST, request.FILES)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            name = reg_form.cleaned_data["name"]
            # 还未在html里加入这个复选框
            introduction = reg_form.cleaned_data["introduction"]
            price = reg_form.cleaned_data["price"]
            avatar = reg_form.cleaned_data['avatar']
            file = reg_form.cleaned_data['file']
            dlc = DLC.objects.create(name=name, price=price, game=game, introduction=introduction, avatar=avatar,
                                     file=file)
            dlc.save()
            # redirect 去的地址要改
            return redirect("game select")
        else:

            context["form"] = DLCRegisterForm()
            # context["clear_errors"] = reg_form.errors.get("__all__")
            return render(request, "add_dlc.html", context)
    else:
        # 是 get
        reg_form = DLCRegisterForm()
        context["form"] = reg_form
        return render(request, "add_dlc.html", context)


def modify_game(request, game_name):
    context = {}
    context.update(csrf(request))
    context['developer'] = get_object_or_404(Developer, user=request.user)
    if request.method == "POST":
        reg_form = GameRegisterForm(request.POST, request.FILES)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            game = Game.objects.filter(name=game_name).get()
            game.name = reg_form.cleaned_data["name"]
            game.game_type = (reg_form.cleaned_data['type'])
            game.introduction = request.POST.get('introduction', game.introduction)
            game.author = Developer.objects.get(user=request.user)
            game.avatar = reg_form.cleaned_data['avatar']
            game.save()
            # redirect 去的地址要改
            return redirect(request.GET.get("from", reverse("home")))
        else:
            context["game"] = Game.objects.filter(name=game_name).get()
            context["form"] = GameRegisterForm()
            return render(request, "modify_game.html", context)
    else:
        # 是 get
        reg_form = GameRegisterForm()
        context["game"] = Game.objects.get(name=game_name)
        context["form"] = reg_form
        return render(request, "modify_game.html", context)


def set_discount(request, game_name):
    # update or create
    context = {}
    context.update(csrf(request))
    game = Game.objects.get(name=game_name)
    dlcs = DLC.objects.filter(game=game)
    developer = get_object_or_404(Developer, user=request.user)
    context["game"] = game
    context["dlcs"] = dlcs
    context['developer'] = developer
    if request.method == "POST":
        form = DiscountRegisterForm(request.POST)
        if form.is_valid():
            # 这里要改
            from_date = form.cleaned_data["from_date"]
            to_date = form.cleaned_data["to_date"]
            price = form.cleaned_data["price"]
            isDLC = form.cleaned_data["is_dlc"]
            if isDLC:
                dlc = form.cleaned_data["dlcs"]
                status = 'DLC'
                discount = Discount.objects.update_or_create(from_date=from_date, to_date=to_date, price=price,
                                                             status=status, dlc=dlc)
            else:
                status = 'GAME'
                discount = Discount.objects.update_or_create(from_date=from_date, to_date=to_date, price=price,
                                                             status=status, game=game)
            discount.save()
            # redirect 去的地址要改
            return redirect(request.GET.get("from", reverse("home")))
        else:
            context["form"] = form
    else:
        form = DiscountRegisterForm()
        context["form"] = form
    return render(request, "set_discount.html", context)


# 加入搜索功能

# 加入购买功能(考虑给user加入余额属性?)
def purchase_game(request, game_name, version_id):
    referer = request.META.get("HTTP_REFERER", reverse("home"))
    # if request.method == 'POST':
    context = {}
    context.update(csrf(request))
    currversion = Version.objects.get(pk=version_id)
    extend = get_object_or_404(ExtendUser, user=request.user)
    # 买了
    # 判断是否购买成功
    success = extend.account > currversion.price
    if success:
        discounts = Discount.objects.filter(game=currversion.game).all()
        flag = True
        for d in discounts:
            if d.from_date < date.today() < d.to_date:
                price = d.price
                flag = False
                break
        if flag:
            price = currversion.price
        extend.account = extend.account - price
        # ExtendUser.objects.filter(id=extend.id).update(account=extend.account - currversion.price)
        developer = currversion.game.author
        developer.account += price
        # Developer.objects.filter(id=developer.id).update(account=developer.account + currversion.price)
        developer.save()
        # game_list = [context]
        # for g in extend.version.all():
        #     game_list.append(g)
        # extend.version.set(game_list)
        extend.version.add(currversion)
        extend.save()
    return redirect(referer)


def purchase_dlc(request, dlc_name, dlc_id):
    # context = {}
    # context.update(csrf(request))
    # dlc = DLC.objects.get(name=dlc_name)
    # context['dlc'] = dlc
    # context['user'] = request.user
    # extend = get_object_or_404(ExtendUser, user=context['user'])
    # if request.method == 'POST':
    #     # 买了
    #     # 判断是否购买成功
    #     success = extend.account > dlc.price
    #     if success:
    #         extend.account = extend.account - dlc.price
    #         developer = dlc.author
    #         developer.account += dlc.price
    #         developer.save()
    #         dlc_list = [dlc]
    #         for g in extend.dlc.all():
    #             dlc_list.append(g)
    #         extend.game.set(game_list)
    #         extend.save()
    #         return redirect("dlc_detail", dlc.pk)
    #     else:
    #         return redirect("purchase fail")
    # else:
    #     return render(request, 'purchase_dlc.html', context)
    referer = request.META.get("HTTP_REFERER", reverse("home"))
    # if request.method == 'POST':
    context = {}
    context.update(csrf(request))
    currdlc = DLC.objects.get(pk=dlc_id)
    extend = get_object_or_404(ExtendUser, user=request.user)
    # 买了
    # 判断是否购买成功
    success = extend.account > currdlc.price
    if success:
        discounts = Discount.objects.filter(dlc=currdlc).all()
        flag = True
        for d in discounts:
            if d.from_date < date.today() < d.to_date:
                price = d.price
                flag = False
                break
        if flag:
            price = currdlc.price
        # extend.account = extend.account - currversion.price
        ExtendUser.objects.filter(id=extend.id).update(account=extend.account - price)
        developer = currdlc.game.author
        # developer.account += currversion.price
        Developer.objects.filter(id=developer.id).update(account=developer.account + price)
        developer.save()
        # game_list = [context]
        # for g in extend.version.all():
        #     game_list.append(g)
        # extend.version.set(game_list)
        extend.dlc.add(currdlc)
        extend.save()
    return redirect(referer)


def add_branch(request, game_name):
    context = {}
    context.update(csrf(request))
    developer = get_object_or_404(Developer, user=request.user)
    game = Game.objects.get(name=game_name)
    context['developer'] = developer
    context['game'] = game
    if request.method == "POST":
        reg_form = BranchRegisterForm(request.POST, request.FILES)
        # 验证过了，说明用户验证也成功了
        if reg_form.is_valid():
            version_num = reg_form.cleaned_data["version_num"]
            introduction = reg_form.cleaned_data["introduction"]
            avatar = reg_form.cleaned_data['avatar']
            file = reg_form.cleaned_data['files']
            price = reg_form.cleaned_data["price"]
            video = reg_form.cleaned_data['video']
            branch = Version.objects.create(version_num=version_num, game=game, introduction=introduction,
                                            avatar=avatar,
                                            file=file, price=price, video=video)
            branch.save()

            # redirect 去的地址要改
            return redirect("game select")
        else:

            context["form"] = BranchRegisterForm()
            # context["clear_errors"] = reg_form.errors.get("__all__")
            return render(request, "add_branch.html", context)
    else:
        # 是 get
        reg_form = BranchRegisterForm()
        context["form"] = reg_form
        return render(request, "add_branch.html", context)


def download_version(request, version_id):
    ver = Version.objects.get(id=version_id)
    img = open(ver.file.url, 'rb').read()
    response = FileResponse(img)
    response['content_type'] = "application/x-shockwave-flash"
    response['Content-Disposition'] = 'attachment; filename=test'
    return response
