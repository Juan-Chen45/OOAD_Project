from django.urls import path
from .views import game_detail, get_game_name, game_list, game_with_date

urlpatterns = [
    path("", game_list, name="game_list"),
    path("<int:game_id>", game_detail, name="game_detail"),
    path("<game_type_name>", get_game_name, name="get_game_name"),
    path("<int:year>/<int:month>", game_with_date, name="game_with_date"),
]
# 在这里定义了名字之后就可以在html中用{% url %}进行引用了
