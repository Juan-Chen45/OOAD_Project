from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    # http://locaohost/8000/blog/1
    path('<str:developer_pk>/', views.home, name='developer_home'),
    path('<str:developer_pk>/games', views.developer_games, name='developer_games'),
    path('<str:developer_pk>/games/<str:game_pk>', views.modify_game_message, name='modify_game_message'),
    path('<str:developer_pk>/addgame', views.add_game, name='add_game'),
    path('<str:developer_pk>/fromUser', views.developer_message, name='developer_message'),
    path('<str:developer_pk>/change_info', views.change_info, name='developer_change_info'),
    path('<str:developer_pk>/setDiscount', views.set_discount, name='set_discount'),
    path('submit', views.change_info_submit, name='developer_change_info_submit'),
]
