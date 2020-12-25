from django.db import models
from django.contrib.auth.models import User
from developer.models import Developer
from read_statistic.models import ReadNum_Expand
from ckeditor_uploader.fields import RichTextUploadingField
from pyquery import PyQuery as pq


# Create your models here.

class GameType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Game(models.Model, ReadNum_Expand):
    name = models.CharField(max_length=50)
    game_type = models.ForeignKey(GameType, on_delete=models.DO_NOTHING)
    introduction = models.TextField(default="")
    author = models.ForeignKey(Developer, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时自动搞时间
    lastupdate_time = models.DateTimeField(auto_now=True)  # 修改时自动改时间
    avatar = models.ImageField(upload_to="game_image/%Y/%m/%d/")

    # price = models.FloatField(default=0)
    # files = models.FileField(upload_to="game_file/%Y/%m/%d/",null=True)
    # versions = []

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


# class Version(models.Model, ReadNum_Expand):
#     name = models.CharField(max_length=50)
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     introduction = models.TextField()
#     create_time = models.DateTimeField(auto_now_add=True)  # 创建时自动搞时间
#     lastupdate_time = models.DateTimeField(auto_now=True)  # 修改时自动改时间
#     avatar = RichTextUploadingField()
#     file = models.FileField()
#
#     def __str__(self):
#         return self.name
#
#     def get_content_img_url(self):
#         temp = Version.objects.filter(pk=str(self.id)).values('avatar')  # values 获取 Article 数据表中的 content 字段内容
#         html = pq(temp[0]['avatar'])  # pq 方法获取编辑器 html 内容
#         # print(html, "\n", "----")
#         img_path = pq(html)('img').attr('src')  # 截取 html 内容中的路径
#         # print("pic", img_path)
#         return img_path  # 返回第一张图片路径
#
#     class Meta:
#         ordering = ["-create_time", ]
class Version(models.Model):
    version_num = models.IntegerField(default=1)
    introduction = models.TextField(default="")
    price = models.FloatField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时自动搞时间
    game = models.ForeignKey(Game, related_name="game_version", on_delete=models.DO_NOTHING)
    avatar = models.ImageField(upload_to="version_image/%Y/%m/%d/")
    file = models.FileField(upload_to="game_file/%Y/%m/%d/", null=True)
    video = models.FileField(upload_to="game_video/%Y/%m/%d/",null=True)
    def __str__(self):
        return self.game.name + str(self.version_num)

    class Meta:
        ordering = ["-create_time", ]


class DLC(models.Model):
    name = models.CharField(max_length=50)
    introduction = models.TextField(default="")
    price = models.FloatField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时自动搞时间
    game = models.ForeignKey(Game, related_name="dlc_version", on_delete=models.DO_NOTHING)
    avatar = models.ImageField(upload_to="dlc_image/%Y/%m/%d/")
    file = models.FileField(upload_to="dlc_file/%Y/%m/%d/", null=True)

    class Meta:
        ordering = ["-create_time", ]

    def __str__(self):
        return self.name


class Discount(models.Model):
    # 加入唯一约束
    GAME = 'GAME'
    DLC = 'DLC'
    STATUS_CHOICES = [
        (GAME, 'GAME'),
        (DLC, 'DLC'),
    ]
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default=GAME,
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    # blank=True null=True
    dlc = models.ForeignKey(DLC, on_delete=models.CASCADE, blank=True, null=True)
    from_date = models.DateField()
    to_date = models.DateField()
    price = models.FloatField()
