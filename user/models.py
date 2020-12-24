from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from pyquery import PyQuery as pq
from game.models import Game, DLC


# Create your models here.
class ExtendUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    introduction = models.CharField(max_length=300, default="大家好！萌新一个！", blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    friend = models.ManyToManyField('self', blank=True)
    game = models.ManyToManyField(Game, blank=True)
    dlc = models.ManyToManyField(DLC, blank=True)
    # 此处修改为ImageField类型
    avatar = models.ImageField(upload_to="avatar/%Y/%m/%d/", default='avatar/defaultAv.png')
    account = models.FloatField(default=0)


    def get_content_img_url(self):
        temp = ExtendUser.objects.filter(pk=str(self.id)).values('avatar')  # values 获取 Article 数据表中的 content 字段内容
        html = pq(temp[0]['avatar'])  # pq 方法获取编辑器 html 内容
        # print(html, "\n", "----")
        img_path = pq(html)('img').attr('src')  # 截取 html 内容中的路径
        # print("pic", img_path)
        return img_path  # 返回第一张图片路径

    def __str__(self):
        return self.user.get_username()

    class Meta:
        ordering = ['create_date', ]
