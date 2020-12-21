from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # http://locaohost/8000/blog/1
    path('', views.developer_home, name='developer_home'),
    path('<str:name>/modify/', views.modify_developer_message, name='modify message'),

]
