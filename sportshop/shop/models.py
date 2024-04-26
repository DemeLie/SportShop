import os
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone

class User(AbstractUser):
    pass

class Categories(models.Model):
    category_name = models.CharField(max_length=64)
    images = models.ImageField(upload_to='images/category_img/', blank=True, null=True)
    def __str__(self):
        return self.category_name
class Item(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(default=timezone.localtime())
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, default=7)
    def __str__(self):
        return self.name
class ItemImages(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.item.name

    def clean(self):
        if self.item.itemimages_set.count() >= 2:
            raise ValidationError("You can upload a maximum of two images per product")

@receiver(post_delete, sender=ItemImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
@receiver(post_delete, sender=Categories)
def auto_delete_file_on_delete_category(sender, instance, **kwargs):
    if instance.images:
        if os.path.isfile(instance.images.path):
            os.remove(instance.images.path)
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=20, default=0, decimal_places=2)
    def __str__(self):
        return self.user.username

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    item_price = models.DecimalField(max_digits=20, default=0, decimal_places=2)


