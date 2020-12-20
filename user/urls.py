from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # http://locaohost/8000/blog/1
    path('', views.user_home, name='user_home'),

]
