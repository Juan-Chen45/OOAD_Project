from read_statistic.models import ReadNum, ReadDetail
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
import datetime
from django.db.models import Sum

def cookie_read(request, object):
    # 下面传参的那个model可以是一个类，也可以是一个类的实例.但contenttype实际上建立的是类之间的外键关系
    # ct = ContentType.objects.get_for_model(object)
    # key = "%s_read" % (object.pk)
    # if not request.COOKIES.get(key):
    #     if ReadNum.objects.filter(content_type=ct, object_id=object.pk).count():
    #         #  存在这个数据
    #         readnum = ReadNum.objects.get(content_type=ct, object_id=object.pk)
    #     else:
    #         # 不存在这个数据
    #         readnum = ReadNum(content_type=ct, object_id=object.pk)
    #     readnum.read_num += 1
    #     readnum.save()
    # return key
    ct = ContentType.objects.get_for_model(object)
    key = "%s_read" % (object.pk)
    if not request.COOKIES.get(key):
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=object.pk)
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=ct, object_id=object.pk, date=date)
        readdetail.read_num += 1
        readdetail.save()

    return key


def get_7days_data(contenttype):
    today = timezone.now().date()
    result_list = []
    date_list = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(i)
        readdetail = ReadDetail.objects.filter(content_type=contenttype,date = date)
        result = readdetail.aggregate(sum = Sum('read_num'))  #返回一个字典
        result_list.append(result['sum'] or 0)   #常用的一个判断，如果前面为false就会返回0，因为你有可能没创建过对应日期的ReadDetail，可能会返回none，none在判断中会为false
        date_list.append(date.strftime("%m/%d"))
    return result_list,date_list


def get_today_hot_data(content_type):
    today = timezone.now().date()
    readdetail = ReadDetail.objects.filter(content_type=content_type, date=today).order_by("read_num")
    # 只返回前7条
    return readdetail[:7]


