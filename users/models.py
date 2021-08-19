from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)
    bio = models.TextField(max_length=100, blank=True)
    #profile_pic = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"{self.user}'s Profile"
