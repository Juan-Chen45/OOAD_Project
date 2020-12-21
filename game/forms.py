from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from game.models import Game


class GameRegisterForm(forms.Form):
    name = forms.CharField(label="游戏名", max_length=20, min_length=3,
                           widget=forms.TextInput(attrs={"placeholder": "请输入游戏名"}))
    price = forms.FloatField(label="价格", min_value=0)
    #avatar = forms.ImageField(label="封面", allow_empty_file=True)

    # 在clean验证的时候其实可以根据每一个不同的字段进行验证的
    def clean_name(self):
        name = self.cleaned_data["name"]
        if Game.objects.filter(name=name).exists():
            raise forms.ValidationError("游戏名已存在")
        return name


class DiscountRegisterForm(forms.Form):
    # blank=True null=True
    from_date = forms.DateField(label="开始时间")
    to_date = forms.DateField(label="结束时间")
    price = forms.FloatField(label="价格", min_value=0)
