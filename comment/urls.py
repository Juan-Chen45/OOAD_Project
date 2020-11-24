from django.urls import path
from .views import update_comment

urlpatterns = [
    path("updatecomment/",update_comment,name = "update_comment"),
]