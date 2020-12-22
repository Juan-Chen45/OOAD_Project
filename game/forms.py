from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from game.models import Game, GameType, DLC


class GameRegisterForm(forms.Form):
    name = forms.CharField(label="游戏名", max_length=20, min_length=3,
                           widget=forms.TextInput(attrs={"placeholder": "请输入游戏名"}))
    price = forms.FloatField(label="价格", min_value=0)
    choices = []
    type_list = GameType.objects.filter().all()
    for type in type_list:
        choices.append((type, type.type_name))
    choices.append((None, "No selection"))
    type = forms.TypedMultipleChoiceField(choices=choices,
                                          coerce=GameType,
                                          empty_value=None,
                                          label="游戏类型")

    # avatar = forms.ImageField(label="封面", allow_empty_file=True)

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
