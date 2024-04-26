from django.contrib import admin
from .models import User, Item, ItemImages, Categories, CartItem, Cart
admin.site.register(User)
admin.site.register(Item)
admin.site.register(ItemImages)
admin.site.register(Categories)
admin.site.register(CartItem)
admin.site.register(Cart)


