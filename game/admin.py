from django.contrib import admin
from .models import Game, GameType, Version, DLC, Discount


# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "game_type", "author", "read_num", "create_time", "lastupdate_time")
    ordering = ("id",)


@admin.register(GameType)
class GameTypeAdmin(admin.ModelAdmin):
    list_display = ("type_name",)


admin.site.register(Version)
admin.site.register(DLC)
admin.site.register(Discount)
