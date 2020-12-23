from django.urls import path
from .views import game_detail, get_game_name, game_list, game_with_date, modify_game, regist_game, set_discount, \
    add_dlc, add_branch

urlpatterns = [
    path("", game_list, name="game_list"),
    path("create", regist_game, name="regist_game"),
    path("<int:game_id>", game_detail, name="game_detail"),
    path("<game_type_name>", get_game_name, name="get_game_name"),
    path("<int:year>/<int:month>", game_with_date, name="game_with_date"),
    path("<str:game_name>/modify", modify_game, name="modify_game"),
    path("<str:game_name>/add_dlc", add_dlc, name="add dlc"),
    path("<str:game_name>/add_branch", add_branch, name="add branch"),
    path("<str:game_name>/discount", set_discount, name="set_discount"),

]
# 在这里定义了名字之后就可以在html中用{% url %}进行引用了
