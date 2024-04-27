from django.contrib import admin
from .models import CartItem, Cart


@admin.register(CartItem)
class AdminCartItem(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'created', 'updated']
    list_filter = ['created', 'updated']


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['id', 'created', 'updated']
