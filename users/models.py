from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10000000)
    music = models.CharField(max_length=10000000)
    

class History(models.Model):
    hist_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    music_id = models.CharField(max_length=10000000, default="")  # Adjusted length and added uniqueness

class Watchlater(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    video_id = models.CharField(max_length=10000000, default="")  # Adjusted length and added uniqueness

class Likedsongs(models.Model):
    watch_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use custom user model
    video_id = models.CharField(max_length=10000000, default="")  # Adjusted length and added uniqueness    


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=2000)
    singer = models.CharField(max_length=2000)
    tags = models.CharField(max_length=100) #pop,classical
    image = models.ImageField(upload_to='images')
    song = models.FileField(upload_to='images')
    movie = models.CharField(max_length=1000, default="")
    credit = models.CharField(max_length=10000000, default="")

    def __str__(self):
        return self.name



# Create your models here.
class CustomUser(AbstractUser):

    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    #description = models.TextField("Description", max_length=600, default='', blank=True)
    
    def __str__(self):
        return self.username


