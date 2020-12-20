from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from django.utils import timezone


# Create your models here.

class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# 方便blog类找到它的readnum
class ReadNum_Expand():
    def read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDetail(models.Model):
    read_num = models.IntegerField(default=0)
    # 注意下面这个now不要加上now(),加上括号之后这个time就是server load model.py 时候的时间
    # 而不加括号这个时间就是你创建这个对象的时间
    date = models.DateField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
