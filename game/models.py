from django.db import models
from django.contrib.auth.models import User
from read_statistic.models import ReadNum_Expand
from ckeditor_uploader.fields import RichTextUploadingField
from pyquery import PyQuery as pq
# Create your models here.

class GameType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Game(models.Model,ReadNum_Expand):
    name = models.CharField(max_length=50)
    game_type = models.ForeignKey(GameType, on_delete=models.DO_NOTHING)
    introduction = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时自动搞时间
    lastupdate_time = models.DateTimeField(auto_now=True)  # 修改时自动改时间
    price = models.FloatField()
    avatar = RichTextUploadingField()

    def get_content_img_url(self):
        temp = Game.objects.filter(pk=str(self.id)).values('avatar')  # values 获取 Article 数据表中的 content 字段内容
        html = pq(temp[0]['avatar'])  # pq 方法获取编辑器 html 内容
        # print(html, "\n", "----")
        img_path = pq(html)('img').attr('src')  # 截取 html 内容中的路径
        # print("pic", img_path)
        return img_path  # 返回第一张图片路径

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-create_time", ]
