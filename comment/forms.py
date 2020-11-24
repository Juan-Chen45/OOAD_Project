from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=CKEditorWidget(config_name="comment_ckeditor"))

    def clean(self):
        try:
            content_type = self.cleaned_data["content_type"]
            object_id = self.cleaned_data["object_id"]
            # 获得博客这个类
            model_class = ContentType.objects.get(model=content_type).model_class()
            content_object = model_class.objects.get(pk=object_id)
            self.cleaned_data["content_object"] = content_object
        except ObjectDoesNotExist as e:
            return forms.ValidationError("评论对象不存在")
        return self.cleaned_data
