from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    followers = models.ManyToManyField('self', blank=True, related_name='user_followers', symmetrical=False)
    following = models.ManyToManyField('self', blank=True, related_name='user_following', symmetrical=False)
    bio = models.TextField(max_length=100, blank=True)
    profile_pic = models.ImageField(upload_to='images/', blank=True)

    @property
    def get_profile_pic_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "media/images/default.png"

    """def save(self, *args, **kwargs):
        # Did we have to resize the image?
        # We pop it to remove from kwargs when we pass these along
        image_resized = kwargs.pop('image_resized', False)

        if self.profile_pic and image_resized:
            basewidth = 100
            filename = self.profile_pic.path
            image = Image.open(filename)
            img = image.resize((basewidth, basewidth), Image.ANTIALIAS)
            self.profile_pic = img
        # Save the updated photo, but inform when we do that we
        # have resized so we don't try and do it again.
            self.save(image_resized=True)

        super(Profile, self).save(*args, **kwargs)"""

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        # saving image first
        super(Profile, self).save(*args, **kwargs)
        if self.profile_pic:

            img = Image.open(self.profile_pic.path)  # Open image using self

            if img.height > 100 or img.width > 100:
                new_img = (100, 100)
                img.thumbnail(new_img)
                img.save(self.profile_pic.path, quality=100)

    def __str__(self):
        return f"{self.user}'s Profile"
