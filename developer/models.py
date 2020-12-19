from ckeditor_uploader.fields import RichTextUploadingField
from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.contrib.auth.models import User
from pyquery import PyQuery as pq

import os
import uuid


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # return the whole path to the file
    return os.path.join("static", "data", "developer", instance.name, filename)


class DocumentationHelp(models.Model):
    documentation = models.TextField()
    url = models.URLField()

    def __str__(self):
        return self.url


class Developer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account = models.CharField(max_length=30)
    introduction = models.CharField(max_length=300)
    create_date = models.DateTimeField().auto_now
    avatar = RichTextUploadingField()

    def get_content_img_url(self):
        temp = Developer.objects.filter(pk=str(self.id)).values('avatar')  # values 获取 Article 数据表中的 content 字段内容
        html = pq(temp[0]['avatar'])  # pq 方法获取编辑器 html 内容
        # print(html, "\n", "----")
        img_path = pq(html)('img').attr('src')  # 截取 html 内容中的路径
        # print("pic", img_path)
        return img_path  # 返回第一张图片路径

    def __str__(self):
        return self.user.get_username()

    class Meta:
        ordering = ['account']
