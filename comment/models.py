from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

# Create your models here.
# 创建一个能评论所有东西的模型
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    # 一对多关系
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ["-create_time",]
