from django.contrib import admin
from .models import Developer, Game, GameShow, GameType, DLC, Version,User,Comment,Vote

# Register your models here.
admin.site.register(Developer)
admin.site.register(GameType)
admin.site.register(Game)
admin.site.register(DLC)
admin.site.register(Version)
admin.site.register(GameShow)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Vote)