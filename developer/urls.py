from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # http://locaohost/8000/blog/1
    path('', views.developer_home, name='developer home'),
    path('modify', views.modify_developer_message, name='modify developer message'),
    path('<str:name>', views.developer_message, name='developer message'),
]
