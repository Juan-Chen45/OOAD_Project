from django.conf.urls import url
from django.urls import path
from .views import user_home

urlpatterns = [
    # http://locaohost/8000/blog/1
    path('', user_home, name='user_home'),

]
