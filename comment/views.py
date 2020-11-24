from django.shortcuts import render,redirect,reverse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import CommentForm
# Create your views here.

def update_comment(request):

    # referer = request.META.get("HTTP_REFERER", reverse("home"))
    # user = request.user
    # # 再多检查一次
    # if not user.is_authenticated:
    #     return render(request, 'error.html', {"message": "用户未登录","redirect_to":referer})
    #
    # text = request.POST.get("comment_text","").strip()
    # if text == '':
    #     return render(request, 'error.html', {"message": "评论内容为空","redirect_to":referer})
    #
    # try:
    #     content_type = request.POST.get("content_type","")
    #     object_id = int(request.POST.get("object_id",""))
    #     # 获得博客这个类
    #     model_class = ContentType.objects.get(model=content_type).model_class()
    #     content_object = model_class.objects.get(pk = object_id)
    # except Exception as e:
    #     return render(request, 'error.html', {"message": "评论对象不存在","redirect_to":referer})
    #
    #
    # comment = Comment()
    # comment.user = user
    # comment.text = text
    # comment.content_object = content_object
    # comment.save()
    # return redirect(referer)

# =============================================现在把判断逻辑放到forms里面去了
    referer = request.META.get("HTTP_REFERER", reverse("home"))
    comment_form = CommentForm(request.POST)
    user = request.user
    # 再多检查一次
    if not user.is_authenticated:
        return render(request, 'error.html', {"message": "用户未登录","redirect_to":referer})
    if comment_form.is_valid():
        # 检查通过
        comment = Comment()
        comment.user = request.user
        comment.text = comment_form.cleaned_data["text"]
        comment.content_object = comment_form.cleaned_data["content_object"]
        comment.save()
        return redirect(referer)
    else:
        return render(request, 'error.html', {"message": comment_form.errors,"redirect_to":referer})
