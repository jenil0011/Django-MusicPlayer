from django.urls import path,include
from . import views



urlpatterns = [
    path('update_song/<int:song_id>/', views.update_song, name='update_song'),  # URL for updating the song
    path('remove_from_watchlater/', views.remove_from_watchlater, name='remove_from_watchlater'),
    path('remove_from_likedsongs/', views.remove_from_likedsongs, name='remove_from_likedsongs'),
    path('search',views.search, name='search'),
    path('upload',views.upload, name='upload'),
    path('c/<str:channel>',views.channel, name='channel'),
    path('history',views.history, name='history'),
    path('watchlater',views.watchlater, name='watchlater'),
    path('likedsongs',views.likedsongs, name='likedsongs'),
    path('songs',views.songs, name='songs'),
    path('songs/<int:id>',views.songpost, name='songpost'),
    path('about/', views.about, name='about'),
    path('', views.homepage, name='homepage'),
    path("register", views.register, name="register"),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('profile/<username>', views.profile, name='profile'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("password_change", views.password_change, name="password_change"),
    path("password_reset", views.password_reset_request, name="password_reset"),
    path('reset/<uidb64>/<token>', views.passwordResetConfirm, name='password_reset_confirm'),

]