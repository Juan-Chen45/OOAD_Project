from django.db import models
from django.contrib.auth.models import User
from read_statistic.models import ReadNum_Expand
from ckeditor_uploader.fields import RichTextUploadingField
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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-create_time", ]
