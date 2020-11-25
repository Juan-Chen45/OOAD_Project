from django.conf.global_settings import MEDIA_ROOT
from django.db import models

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
    name = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    account = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to=user_directory_path, verbose_name='头像', null=True)
    introduction = models.CharField(max_length=300)
    create_date = models.DateTimeField().auto_now

    def __str__(self):
        return self.name
    class Meta:
            ordering = ['account']

class GameType(models.Model):
    type = models.CharField(max_length=10)

class Good(models.Model):
    name=models.CharField(max_length=20,primary_key=True)
    introduction = models.TextField()
    announce_date = models.DateField()
    release_date = models.DateField()
    create_date = models.DateField()
    price = models.FloatField()
    avatar = models.ImageField(upload_to=user_directory_path, verbose_name='封面', null=True)
    def __str__(self):
        return self.name
    class Meta :
        abstract = True


class Game(Good):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE,related_name='game_developer_set')
    type=models.ManyToManyField(GameType)
    def __str__(self):
        return self.name


class DLC(Good):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    file=models.FileField()
    def __str__(self):
        return self.name


class Version(Good):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    file=models.FileField()
    def __str__(self):
        return self.name

class GameShow(models.Model):
    file = models.ImageField()
    game= models.ForeignKey(Game,on_delete=models.CASCADE,blank=True,null=True)
    #blank=True null=True
    version=models.ForeignKey(Version,on_delete=models.CASCADE,blank=True,null=True)
    dlc=models.ForeignKey(DLC,on_delete=models.CASCADE,blank=True,null=True)
    VERSION = 'VERSION'
    GAME = 'GAME'
    DLC='DLC'
    STATUS_CHOICES = [
        (VERSION , 'VERSION'),
        (GAME , 'GAME'),
        (DLC,'DLC'),
    ]
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default=GAME,
    )

class User(models.Model):
    password = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20)
    account = models.FloatField()
    avatar = models.ImageField()
    introduction = models.TextField()
    create_date = models.DateField()
    game = models.ManyToManyField(Game)
    dlc = models.ManyToManyField(DLC)

    def __str__(self):
        return self.user_name


class Comment(models.Model):
    content = models.TextField()
    create_user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField()
    # if it is false it is a comment to comment
    is_to_game = models.BooleanField()
    game= models.ForeignKey(Game,on_delete=models.CASCADE,blank=True,null=True)
    #blank=True null=True
    version=models.ForeignKey(Version,on_delete=models.CASCADE,blank=True,null=True)
    dlc=models.ForeignKey(DLC,on_delete=models.CASCADE,blank=True,null=True)
    comment_fk = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    VERSION = 'VERSION'
    GAME = 'GAME'
    DLC='DLC'
    STATUS_CHOICES = [
        (VERSION , 'VERSION'),
        (GAME , 'GAME'),
        (DLC,'DLC'),
    ]
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default=GAME,
    )
    class Meta:
        ordering = ['-create_time']
    def __str__(self):
        return self.content

class Vote(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    comment = models.ForeignKey(Comment, models.CASCADE)
    is_up = models.BooleanField()

#忘写discount 了,要加上
class Discount(models.Model):
    VERSION = 'VERSION'
    GAME = 'GAME'
    DLC='DLC'
    STATUS_CHOICES = [
        (VERSION , 'VERSION'),
        (GAME , 'GAME'),
        (DLC,'DLC'),
    ]
    status = models.CharField(
        max_length=7,
        choices=STATUS_CHOICES,
        default=GAME,
    )
    game= models.ForeignKey(Game,on_delete=models.CASCADE,blank=True,null=True)
    #blank=True null=True
    version=models.ForeignKey(Version,on_delete=models.CASCADE,blank=True,null=True)
    dlc=models.ForeignKey(DLC,on_delete=models.CASCADE,blank=True,null=True)
    from_date=models.DateField()
    to_date=models.DateField()
    price=models.FloatField()