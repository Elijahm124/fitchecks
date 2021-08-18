from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid


class Closet(models.Model):
    style = models.CharField(max_length=50, default="main_closet")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False)

    def __str__(self):
        if " " in self.style:
            return "".join(self.style)
        return self.style


class Fit(models.Model):
    """An Outfit"""
    description = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/')
    tags = models.CharField(max_length=100, blank=True)
    closet = models.ManyToManyField(Closet)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    shown_id = models.CharField(max_length=32, primary_key=False, default=uuid.uuid4().hex[:8], editable=False)
    private = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super().save()  # saving image first

        img = Image.open(self.image.path)  # Open image using self

        if img.height > 500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.image.path, quality=100)

    def __str__(self):
        return self.description[:10]


"""class Top(models.Model):
    style = models.CharField()
    size = models.CharField(max_length=15)
    color = models.CharField(max_length=20)"""
