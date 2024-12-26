from django.contrib import admin
from .models import CustomUser
from .models import Song,Watchlater,History,Channel,Likedsongs

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Song)
admin.site.register(Watchlater)
admin.site.register(Likedsongs)
admin.site.register(History)
admin.site.register(Channel)



