from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf

from user.models import ExtendUser
from game.models import Game
from django.contrib.auth.models import User
from user.forms import UserModifyForm
from django.urls import reverse
from myfirstsite.views import user_login


# Create your views here.


def writeFile(filePath, file):
    with open(filePath, "wb") as f:
        if file.multiple_chunks():
            for content in file.chunks():
                f.write(content)
        else:
            data = file.read().decode('utf-8')
            f.write(data)


def uploadFile(request):
    if request.method == "POST":
        fileDict = request.FILES.items()
        # 获取上传的文件，如果没有文件，则默认为None
        if not fileDict:
            return JsonResponse({'msg': 'no file upload'})
        for (k, v) in fileDict:
            print("dic[%s]=%s" % (k, v))
            fileData = request.FILES.getlist(k)
            for file in fileData:
                fileName = file._get_name()
                filePath = os.path.join(settings.TEMP_FILE_PATH, fileName)
                print('filepath = [%s]' % filePath)
                try:
                    writeFile(filePath, file)
                except:
                    return JsonResponse({'msg': 'file write failed'})
        return JsonResponse({'msg': 'success'})


def user_home(request):
    context = {}
    context['user'] = request.user

    if request.user.is_authenticated:
        context['extendUser'] = ExtendUser.objects.get(user=request.user)
        context['games'] = context['extendUser'].game.all()
        return render(request, 'user_home.html', context)
    else:
        return user_login(request)


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
