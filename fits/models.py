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
    shown_id = models.CharField(max_length=32, primary_key=False, default=uuid.uuid4().hex[:8], editable=False,
                                unique=True)
    private = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, *args, **kwargs):
        # saving image first
        super(Fit, self).save(*args, **kwargs)

        img = Image.open(self.image.path)  # Open image using self

        if img.height > 500 or img.width > 500:
            new_img = (500, 500)
            img.thumbnail(new_img)
            img.save(self.image.path, quality=100)

    def __str__(self):
        return self.description[:10]


class Top(models.Model):
    brand = models.CharField(max_length=30, blank=True)
    size = models.CharField(max_length=15, blank=True)
    color = models.CharField(max_length=20, blank=True)
    description = models.CharField(max_length=50, blank=True)
    price = models.IntegerField(default=0)
    fit = models.ForeignKey(Fit, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.description[:10]


class Bottom(models.Model):
    brand = models.CharField(max_length=30)
    size = models.CharField(max_length=15)
    color = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    fit = models.OneToOneField(Fit, on_delete=models.CASCADE)

    def __str__(self):
        return self.description[:10]


class Accessory(models.Model):
    brand = models.CharField(max_length=30)
    size = models.CharField(max_length=15)
    color = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    fit = models.ForeignKey(Fit, on_delete=models.CASCADE)

    def __str__(self):
        return self.description[:10]


class Shoe(models.Model):
    brand = models.CharField(max_length=30)
    size = models.CharField(max_length=15)
    color = models.CharField(max_length=20)
    description = models.CharField(max_length=50)
    price = models.IntegerField()
    fit = models.OneToOneField(Fit, on_delete=models.CASCADE)

    def __str__(self):
        return self.description[:10]
