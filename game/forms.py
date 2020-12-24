from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.core import validators

from game.models import Game, GameType, DLC, Version

class GameRegisterForm(forms.Form):
    name = forms.CharField(label="游戏名", max_length=20, min_length=3,
                           widget=forms.TextInput(attrs={"placeholder": "请输入游戏名"}))
    price = forms.FloatField(label="价格", min_value=0)
    avatar = forms.ImageField(label="封面")
    type = forms.ModelChoiceField(label="游戏类型",queryset=GameType.objects.all())
    files = forms.FileField(validators=[validators.FileExtensionValidator(['swf'])])
    introduction = forms.CharField(widget=forms.Textarea(attrs={'width':"40%", 'cols' : "80", 'rows': "20", }))

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
    is_dlc = forms.TypedChoiceField(label='对象是否为dlc',
                                    widget=forms.RadioSelect,
                                    choices=[(True, "是"), (False, "否")],
                                    empty_value=False,
                                    coerce=bool,
                                    )
    dlcs = forms.TypedChoiceField()

    def set_fields(self, dlc_list):
        choices = []
        for dlc in dlc_list:
            choices.append((dlc, dlc.name))

        if len(dlc_list) == 0:
            choices.append((None, "No selection"))

        self.dlcs = forms.TypedChoiceField(
            label="选择dlc",
            widget=forms.RadioSelect,
            choices=choices,
            empty_value=None,
            coerce=DLC,
        )


class DLCRegisterForm(forms.Form):
    name = forms.CharField(label="dlc名", max_length=20, min_length=3,
                           widget=forms.TextInput(attrs={"placeholder": "请输入dlc名"}))
    price = forms.FloatField(label="价格", min_value=0)
    avatar = forms.ImageField(label="封面")
    introduction = forms.CharField(label="dlc介绍")
    file = forms.FileField(label="选择dlc文件")

    def clean_name(self):
        name = self.cleaned_data["name"]
        if DLC.objects.filter(name=name).exists():
            raise forms.ValidationError("dlc名已存在")
        return name


class BranchRegisterForm(forms.Form):
    name = forms.CharField(label="branch名", max_length=20, min_length=3,
                           widget=forms.TextInput(attrs={"placeholder": "请输入branch名"}))
    avatar = forms.ImageField(label="封面")
    introduction = forms.CharField(label="branch介绍")
    file = forms.FileField(label="选择branch文件")

    def clean_name(self):
        name = self.cleaned_data["name"]
        if Version.objects.filter(name=name).exists():
            raise forms.ValidationError("dlc名已存在")
        return name
